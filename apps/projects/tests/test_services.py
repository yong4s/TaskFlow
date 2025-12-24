from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.projects.services import ProjectService
from apps.utils.exceptions import ObjectNotFoundError
from apps.utils.exceptions import PermissionDeniedError
from apps.utils.exceptions import ValidationError

User = get_user_model()

TEST_PASSWORD = 'testpass123'  # noqa: S105


class TestProjectService(TestCase):
    """Essential tests for ProjectService business logic."""

    def setUp(self):
        self.mock_dal = Mock()
        self.mock_validator = Mock()
        self.user = Mock()
        self.user.id = 1
        self.user.email = 'test@example.com'

        self.service = ProjectService(project_dal=self.mock_dal, validator=self.mock_validator)

    def test_create_project_success(self):
        """Test successful project creation with valid data."""
        raw_name = ' Test Project '
        clean_name = 'Test Project'

        created_project_mock = Mock()
        created_project_mock.id = 1
        created_project_mock.name = clean_name

        self.mock_validator.validate_create_project.return_value = clean_name

        queryset_mock = Mock()
        queryset_mock.exists.return_value = False
        self.mock_dal.filter_by.return_value = queryset_mock
        self.mock_dal.create.return_value = created_project_mock

        result = self.service.create_project(user=self.user, name=raw_name)

        self.mock_validator.validate_create_project.assert_called_once_with(raw_name, queryset_mock)
        self.mock_dal.filter_by.assert_called_once_with(user=self.user, name__iexact=raw_name)
        self.mock_dal.create.assert_called_once_with(user=self.user, name=clean_name)
        self.assertEqual(result, created_project_mock)

    def test_create_project_duplicate_name(self):
        """Test project creation fails with duplicate name."""
        name = 'Duplicate Project'

        queryset_mock = Mock()
        queryset_mock.exists.return_value = True  # Duplicate found
        self.mock_dal.filter_by.return_value = queryset_mock

        self.mock_validator.validate_create_project.side_effect = ValidationError(
            'name', 'Project with this name already exists'
        )

        with self.assertRaises(ValidationError) as cm:
            self.service.create_project(user=self.user, name=name)

        self.assertEqual(str(cm.exception), 'Validation error for field "name": Project with this name already exists')
        self.mock_dal.create.assert_not_called()

    def test_update_project_permission_denied(self):
        """Test update fails when user doesn't own project."""
        project_id = 1
        project_mock = Mock()
        project_mock.id = project_id
        project_mock.user = Mock(id=999)

        self.mock_dal.get_by_id.return_value = project_mock
        self.mock_validator.validate_update_project_name.side_effect = PermissionDeniedError(
            'You can only access your own projects'
        )

        with self.assertRaises(PermissionDeniedError):
            self.service.update_project(user=self.user, project_id=project_id, name='New Name')

        self.mock_dal.update.assert_not_called()

    def test_delete_project_not_found(self):
        """Test delete fails when project doesn't exist."""
        project_id = 999
        self.mock_dal.get_by_id.side_effect = ObjectNotFoundError('Project', project_id)

        with self.assertRaises(ObjectNotFoundError):
            self.service.delete_project(user=self.user, project_id=project_id)

        self.mock_dal.delete.assert_not_called()


class TestProjectServiceIntegration(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password=TEST_PASSWORD)
        self.other_user = User.objects.create_user(email='other@example.com', password=TEST_PASSWORD)
        self.service = ProjectService()

    def test_full_project_lifecycle(self):
        """Test complete project lifecycle: create, update, delete."""
        project = self.service.create_project(self.user, 'Test Project')
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.user, self.user)

        updated_project = self.service.update_project(self.user, project.id, name='Updated Project')
        self.assertEqual(updated_project.name, 'Updated Project')

        self.service.delete_project(self.user, project.id)

        with self.assertRaises(ObjectNotFoundError):
            self.service.get_user_project(self.user, project.id)

    def test_user_isolation(self):
        """Test that users can only access their own projects."""
        project = self.service.create_project(self.user, 'My Project')

        with self.assertRaises(PermissionDeniedError):
            self.service.update_project(self.other_user, project.id, name='Hacked')

        with self.assertRaises(PermissionDeniedError):
            self.service.delete_project(self.other_user, project.id)

    def test_name_uniqueness_per_user(self):
        """Test name uniqueness constraint per user."""
        self.service.create_project(self.user, 'Same Name')
        with self.assertRaises(ValidationError):
            self.service.create_project(self.user, 'Same Name')

        self.service.create_project(self.other_user, 'Same Name')
