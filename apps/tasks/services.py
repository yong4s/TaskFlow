import logging
from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import Model, QuerySet

from apps.tasks.dal import TaskRepository
from apps.tasks.models import Task
from apps.tasks.validators import TaskValidator

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.services import ProjectService


class TaskService:
    def __init__(self, task_dal=None, project_service=None, validator=None):
        self.task_dal = task_dal or TaskRepository()
        self.validator = validator or TaskValidator()
        # Lazy import to avoid circular dependencies
        self._project_service = project_service

    @property
    def project_service(self) -> 'ProjectService':
        if self._project_service is None:
            from apps.projects.services import ProjectService

            self._project_service = ProjectService()
        return self._project_service

    def create_task(self, user: 'User', project_id: int, title: str, deadline=None) -> Model:
        project = self.project_service.get_user_project(user, project_id)
        clean_title = self.validator.validate_create_task(title)

        task = self.task_dal.create(
            name=clean_title,
            project=project,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM,
            deadline=deadline
        )

        logger.info(r"Task created: %s \%s' by user %s", task.id, clean_title, user.id)
        return task

    def update_task(self, user: 'User', task_id: int, **kwargs) -> Model:
        task = self.task_dal.get_by_id(task_id)

        validated_data = self.validator.validate_update_task(
            user, task, title=kwargs.get('title'), priority=kwargs.get('priority'), deadline=kwargs.get('deadline')
        )

        kwargs.pop('title', None)
        kwargs.update(validated_data)

        updated_task = self.task_dal.update(task, **kwargs)
        logger.info('Task updated: %s by user %s', task_id, user.id)
        return updated_task

    def delete_task(self, user: 'User', task_id: int) -> None:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_delete_task(user, task)
        self.task_dal.delete(task)
        logger.info('Task deleted: %s by user %s', task_id, user.id)

    def complete_task(self, user: 'User', task_id: int) -> Model:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_complete_task(user, task)
        return self.task_dal.update(task, status=Task.Status.DONE)

    def set_priority(self, user: 'User', task_id: int, priority: int) -> Model:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_set_priority(user, task, priority)
        return self.task_dal.update(task, priority=priority)

    def set_deadline(self, user: 'User', task_id: int, deadline: datetime) -> Model:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_set_deadline(user, task, deadline)
        return self.task_dal.update(task, deadline=deadline)

    def get_user_tasks(self, user: 'User') -> QuerySet:
        return self.task_dal.get_by_user(user)

    def toggle_task_status(self, user: 'User', task_id: int) -> Model:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_ownership(user, task)

        new_status = Task.Status.IN_PROGRESS if task.status == Task.Status.DONE else Task.Status.DONE
        updated_task = self.task_dal.update(task, status=new_status)
        logger.info('Task status toggled: %s to %s by user %s', task_id, new_status, user.id)
        return updated_task


    def get_user_task(self, user: 'User', task_id: int) -> Model:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_ownership(user, task)
        return task

    def get_project_tasks_sorted(self, user: 'User', project_id: int) -> QuerySet:
        project = self.project_service.get_user_project(user, project_id)
        return self.task_dal.get_by_project_sorted(project)
