from typing import List, Optional, TYPE_CHECKING

from apps.utils.exceptions import PermissionDeniedError, ValidationError

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.models import Project


class ProjectValidator:
    """Handles project validation and business rules."""
    MAX_NAME_LENGTH = 255

    def validate_name_format(self, name: str) -> str:
        name = name.strip()

        if not name:
            field = 'name'
            message = 'Project name cannot be empty'
            raise ValidationError(field, message)

        if len(name) > self.MAX_NAME_LENGTH:
            field = 'name'
            message = f'Project name too long (max {self.MAX_NAME_LENGTH} characters)'
            raise ValidationError(field, message)

        return name

    def validate_ownership(self, user: 'User', project: 'Project'):
        if project.user != user:
            message = 'You can only access your own projects'
            raise PermissionDeniedError(message)

    def validate_delete_project(self, user: 'User', project: 'Project'):
        self.validate_ownership(user, project)

    def validate_access_project(self, user: 'User', project: 'Project'):
        self.validate_ownership(user, project)

    def validate_create_project(self, name: str, existing_projects_query) -> str:
        """Complete validation for project creation."""
        clean_name = self.validate_name_format(name)

        if existing_projects_query.exists():
            msg = 'name'
            raise ValidationError(msg, 'Project with this name already exists')

        return clean_name

    def validate_update_project_name(self, user: 'User', project: 'Project', name: str, existing_projects_query) -> str:
        """Complete validation for project name update."""
        self.validate_ownership(user, project)
        clean_name = self.validate_name_format(name)

        if existing_projects_query.exists():
            msg = 'name'
            raise ValidationError(msg, 'Project with this name already exists')

        return clean_name
