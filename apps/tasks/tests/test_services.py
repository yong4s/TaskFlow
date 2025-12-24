from datetime import timedelta
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.tasks.models import Task
from apps.tasks.services import TaskService
from apps.utils.exceptions import BusinessRuleError
from apps.utils.exceptions import PermissionDeniedError
from apps.utils.exceptions import ValidationError

User = get_user_model()

TEST_PASSWORD = 'testpass123'  # noqa: S105


class TestTaskService(TestCase):
    """Essential tests for TaskService business logic."""

    def setUp(self):
        self.mock_dal = Mock()
        self.mock_validator = Mock()
        self.mock_project_service = Mock()
        self.user = Mock()
        self.user.id = 1
        self.user.email = 'test@example.com'

        self.service = TaskService(
            task_dal=self.mock_dal, project_service=self.mock_project_service, validator=self.mock_validator
        )

    def test_create_task_success(self):
        """Test successful task creation with valid data."""
        project_id = 1
        title = 'Test Task'
        clean_title = 'Test Task'

        project_mock = Mock()
        project_mock.id = project_id

        created_task_mock = Mock()
        created_task_mock.id = 1
        created_task_mock.name = clean_title

        self.mock_project_service.get_user_project.return_value = project_mock
        self.mock_validator.validate_create_task.return_value = clean_title
        self.mock_dal.create.return_value = created_task_mock

        result = self.service.create_task(self.user, project_id, title)

        self.mock_project_service.get_user_project.assert_called_once_with(self.user, project_id)
        self.mock_validator.validate_create_task.assert_called_once_with(title)
        self.mock_dal.create.assert_called_once_with(
            name=clean_title, project=project_mock, status=Task.Status.NEW, priority=Task.Priority.MEDIUM, deadline=None
        )
        self.assertEqual(result, created_task_mock)

    def test_complete_task_already_done(self):
        """Test completion fails when task already completed."""
        task_id = 1
        task_mock = Mock()
        task_mock.id = task_id
        task_mock.status = Task.Status.DONE

        self.mock_dal.get_by_id.return_value = task_mock
        self.mock_validator.validate_complete_task.side_effect = BusinessRuleError('Task is already completed')

        with self.assertRaises(BusinessRuleError):
            self.service.complete_task(self.user, task_id)

        self.mock_dal.update.assert_not_called()

    def test_update_task_permission_denied(self):
        """Test update fails when user doesn't own task."""
        task_id = 1
        task_mock = Mock()
        task_mock.id = task_id
        task_mock.project.user = Mock(id=999)

        self.mock_dal.get_by_id.return_value = task_mock
        self.mock_validator.validate_update_task.side_effect = PermissionDeniedError(
            'You can only update tasks in your own projects'
        )

        with self.assertRaises(PermissionDeniedError):
            self.service.update_task(self.user, task_id, title='New Title')

        self.mock_dal.update.assert_not_called()

    def test_set_deadline_past_date(self):
        """Test set deadline fails with past date."""
        task_id = 1
        past_deadline = timezone.now() - timedelta(days=1)
        task_mock = Mock()
        task_mock.id = task_id

        self.mock_dal.get_by_id.return_value = task_mock
        self.mock_validator.validate_set_deadline.side_effect = ValidationError(
            'deadline', 'Deadline cannot be in the past'
        )

        with self.assertRaises(ValidationError):
            self.service.set_deadline(self.user, task_id, past_deadline)

        self.mock_dal.update.assert_not_called()

    def test_get_user_task_success(self):
        """Test successful task retrieval with permission check."""
        task_id = 1
        task_mock = Mock()
        task_mock.id = task_id

        self.mock_dal.get_by_id.return_value = task_mock
        self.mock_validator.validate_ownership.return_value = None

        result = self.service.get_user_task(self.user, task_id)

        self.mock_dal.get_by_id.assert_called_once_with(task_id)
        self.mock_validator.validate_ownership.assert_called_once_with(self.user, task_mock)
        self.assertEqual(result, task_mock)

    def test_get_user_task_permission_denied(self):
        """Test get task fails when user doesn't own task."""
        task_id = 1
        task_mock = Mock()
        task_mock.id = task_id

        self.mock_dal.get_by_id.return_value = task_mock
        self.mock_validator.validate_ownership.side_effect = PermissionDeniedError(
            'You can only access tasks in your own projects'
        )

        with self.assertRaises(PermissionDeniedError):
            self.service.get_user_task(self.user, task_id)


class TestTaskServiceIntegration(TestCase):
    """Integration tests with real database."""

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password=TEST_PASSWORD)
        self.other_user = User.objects.create_user(email='other@example.com', password=TEST_PASSWORD)

        from apps.projects.services import ProjectService

        project_service = ProjectService()
        self.project = project_service.create_project(self.user, 'Test Project')
        self.other_project = project_service.create_project(self.other_user, 'Other Project')

        self.service = TaskService()

    def test_full_task_lifecycle(self):
        """Test complete task lifecycle: create, update, complete."""
        task = self.service.create_task(self.user, self.project.id, 'Test Task')
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.status, Task.Status.NEW)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

        updated_task = self.service.set_priority(self.user, task.id, Task.Priority.HIGH)
        self.assertEqual(updated_task.priority, Task.Priority.HIGH)

        future_deadline = timezone.now() + timedelta(days=7)
        deadline_task = self.service.set_deadline(self.user, task.id, future_deadline)
        self.assertEqual(deadline_task.deadline.date(), future_deadline.date())

        completed_task = self.service.complete_task(self.user, task.id)
        self.assertEqual(completed_task.status, Task.Status.DONE)

    def test_user_isolation(self):
        """Test that users can only access their own tasks."""
        task = self.service.create_task(self.user, self.project.id, 'My Task')

        with self.assertRaises(PermissionDeniedError):
            self.service.update_task(self.other_user, task.id, title='Hacked')

        with self.assertRaises(PermissionDeniedError):
            self.service.delete_task(self.other_user, task.id)

        with self.assertRaises(PermissionDeniedError):
            self.service.complete_task(self.other_user, task.id)

    def test_project_access_control(self):
        """Test task creation respects project ownership."""
        with self.assertRaises(PermissionDeniedError):
            self.service.create_task(self.user, self.other_project.id, 'Unauthorized Task')

    def test_task_status_transitions(self):
        """Test valid task status transitions."""
        task = self.service.create_task(self.user, self.project.id, 'Test Task')

        completed_task = self.service.complete_task(self.user, task.id)
        self.assertEqual(completed_task.status, Task.Status.DONE)

        with self.assertRaises(BusinessRuleError):
            self.service.complete_task(self.user, task.id)
