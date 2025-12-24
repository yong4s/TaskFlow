import logging
from typing import TYPE_CHECKING

from django.db.models import QuerySet

from apps.projects.dal import ProjectRepository
from apps.projects.validators import ProjectValidator
from apps.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.models import Project


class ProjectService:
    def __init__(self, project_dal=None, validator=None):
        self.project_dal = project_dal or ProjectRepository()
        self.validator = validator or ProjectValidator()

    def create_project(self, user: 'User', name: str) -> 'Project':
        existing_projects = self.project_dal.filter_by(user=user, name__iexact=name)
        clean_name = self.validator.validate_create_project(name, existing_projects)
        project = self.project_dal.create(user=user, name=clean_name)
        logger.info(r"Project created: %s \%s' by user %s", project.id, clean_name, user.id)
        return project

    def update_project(self, user: 'User', project_id: int, **kwargs) -> 'Project':
        project = self.project_dal.get_by_id(project_id)

        if 'name' in kwargs:
            existing_projects = self.project_dal.filter_by(user=user, name__iexact=kwargs['name']).exclude(
                id=project.id
            )

            clean_name = self.validator.validate_update_project_name(user, project, kwargs['name'], existing_projects)
            kwargs['name'] = clean_name
        else:
            self.validator.validate_ownership(user, project)

        return self.project_dal.update(project, **kwargs)

    def delete_project(self, user: 'User', project_id: int) -> None:
        project = self.project_dal.get_by_id(project_id)
        self.validator.validate_delete_project(user, project)
        self.project_dal.delete(project)
        logger.info('Project deleted: %s by user %s', project_id, user.id)

    def get_user_projects(self, user: 'User') -> QuerySet:
        return self.project_dal.get_by_user(user)

    def get_user_projects_with_tasks(self, user: 'User') -> QuerySet:
        return self.project_dal.get_by_user_with_tasks(user)

    def get_user_project(self, user: 'User', project_id: int) -> 'Project':
        project = self.project_dal.get_by_id(project_id)
        self.validator.validate_access_project(user, project)
        return project
