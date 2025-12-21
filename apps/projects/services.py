from typing import TYPE_CHECKING

from django.db.models import QuerySet

from .dal import ProjectRepository
from .validators import ProjectValidator

if TYPE_CHECKING:
    from apps.accounts.models import User
    from .models import Project


class ProjectService:
    """Service layer for project-related business operations."""

    def __init__(self, project_dal=None, validator=None):
        self.project_dal = project_dal or ProjectRepository()
        self.validator = validator or ProjectValidator()

    def create_project(self, user: 'User', name: str) -> 'Project':
        existing_projects = list(self.project_dal.get_by_user(user))
        clean_name = self.validator.validate_create_project(user, name, existing_projects)
        return self.project_dal.create(user=user, name=clean_name)

    def update_project(self, user: 'User', project_id: int, **kwargs) -> 'Project':
        """Update project with permission checks."""
        project = self.project_dal.get_by_id(project_id)
        
        # Validate name if provided
        if 'name' in kwargs:
            existing_projects = list(self.project_dal.get_by_user(user))
            clean_name = self.validator.validate_update_project(user, project, existing_projects, kwargs['name'])
            if clean_name:
                kwargs['name'] = clean_name
        else:
            self.validator.validate_ownership(user, project)

        return self.project_dal.update(project, **kwargs)

    def delete_project(self, user: 'User', project_id: int) -> None:
        project = self.project_dal.get_by_id(project_id)
        self.validator.validate_delete_project(user, project)
        self.project_dal.delete(project)

    def get_user_projects(self, user: 'User') -> QuerySet:
        return self.project_dal.get_by_user(user)

    def get_user_project(self, user: 'User', project_id: int) -> 'Project':
        project = self.project_dal.get_by_id(project_id)
        self.validator.validate_access_project(user, project)
        return project

