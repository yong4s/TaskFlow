from typing import TYPE_CHECKING
from datetime import datetime
from django.utils import timezone
from django.db.models import QuerySet

from apps.utils.exceptions import PermissionDeniedError, ValidationError, BusinessRuleError
from .dal import TaskRepository
from .models import Task
from .validators import TaskValidator

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.services import ProjectService


class TaskService:
    """Service layer for task-related business operations."""
    
    def __init__(self, task_dal=None, project_service=None, validator=None):
        self.task_dal = task_dal or TaskRepository()
        self.validator = validator or TaskValidator()
        # Lazy import to avoid circular dependencies
        self._project_service = project_service
    
    @property
    def project_service(self) -> 'ProjectService':
        """Lazy loading of ProjectService to avoid circular imports."""
        if self._project_service is None:
            from apps.projects.services import ProjectService
            self._project_service = ProjectService()
        return self._project_service
    
    def create_task(self, user: 'User', project_id: int, title: str, description: str = '') -> Task:
        """Create new task in project."""
        # Get project and validate access
        project = self.project_service.get_user_project(user, project_id)
        
        # Validate task data
        clean_title = self.validator.validate_create_task(user, title, description)
        
        return self.task_dal.create(
            name=clean_title,
            description=description,
            project=project,
            status=Task.Status.NEW,
            priority=Task.Priority.MEDIUM
        )
    
    def update_task(self, user: 'User', task_id: int, **kwargs) -> Task:
        """Update task with permission checks."""
        task = self.task_dal.get_by_id(task_id)
        
        # Validate and clean data
        validated_data = self.validator.validate_update_task(
            user, 
            task,
            title=kwargs.get('title'),
            priority=kwargs.get('priority'),
            deadline=kwargs.get('deadline')
        )
        
        # Update kwargs with validated data
        kwargs.update(validated_data)
        if 'title' in kwargs:
            del kwargs['title']  # Remove title since we added 'name'
        
        return self.task_dal.update(task, **kwargs)
    
    def delete_task(self, user: 'User', task_id: int) -> None:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_delete_task(user, task)
        self.task_dal.delete(task)
    
    def complete_task(self, user: 'User', task_id: int) -> Task:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_complete_task(user, task)
        return self.task_dal.update(task, status=Task.Status.DONE)
    
    def set_priority(self, user: 'User', task_id: int, priority: int) -> Task:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_set_priority(user, task, priority)
        return self.task_dal.update(task, priority=priority)
    
    def set_deadline(self, user: 'User', task_id: int, deadline: datetime) -> Task:
        task = self.task_dal.get_by_id(task_id)
        self.validator.validate_set_deadline(user, task, deadline)
        return self.task_dal.update(task, deadline=deadline)
    
    def get_user_tasks(self, user: 'User') -> QuerySet:
        return self.task_dal.get_by_user(user)