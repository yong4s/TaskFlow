from typing import TYPE_CHECKING
from datetime import datetime
from django.utils import timezone

from apps.utils.exceptions import PermissionDeniedError, ValidationError, BusinessRuleError

if TYPE_CHECKING:
    from apps.accounts.models import User
    from .models import Task


class TaskValidator:

    MAX_TITLE_LENGTH = 255
    MIN_PRIORITY = 1
    MAX_PRIORITY = 5
    
    def validate_title_format(self, title: str) -> str:
        title = title.strip()
        
        if not title:
            field = 'title'
            message = 'Task title cannot be empty'
            raise ValidationError(field, message)
        
        if len(title) > self.MAX_TITLE_LENGTH:
            field = 'title'
            message = f'Task title too long (max {self.MAX_TITLE_LENGTH} characters)'
            raise ValidationError(field, message)
        
        return title
    
    def validate_priority(self, priority: int):
        if not isinstance(priority, int) or priority < self.MIN_PRIORITY or priority > self.MAX_PRIORITY:
            field = 'priority'
            message = f'Priority must be between {self.MIN_PRIORITY} and {self.MAX_PRIORITY}'
            raise ValidationError(field, message)
    
    def validate_deadline(self, deadline: datetime):
        if deadline < timezone.now():
            field = 'deadline'
            message = 'Deadline cannot be in the past'
            raise ValidationError(field, message)
    
    def validate_ownership(self, user: 'User', task: 'Task'):
        if task.project.user != user:
            message = 'You can only access tasks in your own projects'
            raise PermissionDeniedError(message)
    
    def validate_task_completion(self, task: 'Task'):
        if task.status == task.Status.DONE:
            message = 'Task is already completed'
            raise BusinessRuleError(message)
    
    def validate_create_task(self, user: 'User', title: str, description: str = '') -> str:
        """Complete validation for task creation."""
        clean_title = self.validate_title_format(title)
        return clean_title
    
    def validate_update_task(self, user: 'User', task: 'Task', title: str = None, priority: int = None, deadline: datetime = None) -> dict:
        """Complete validation for task update."""
        self.validate_ownership(user, task)
        
        validated_data = {}
        
        if title is not None:
            validated_data['name'] = self.validate_title_format(title)
        
        if priority is not None:
            self.validate_priority(priority)
            validated_data['priority'] = priority
        
        if deadline is not None:
            self.validate_deadline(deadline)
            validated_data['deadline'] = deadline
        
        return validated_data
    
    def validate_delete_task(self, user: 'User', task: 'Task'):
        self.validate_ownership(user, task)
    
    def validate_complete_task(self, user: 'User', task: 'Task'):
        self.validate_ownership(user, task)
        self.validate_task_completion(task)
    
    def validate_set_priority(self, user: 'User', task: 'Task', priority: int):
        self.validate_ownership(user, task)
        self.validate_priority(priority)
    
    def validate_set_deadline(self, user: 'User', task: 'Task', deadline: datetime):
        self.validate_ownership(user, task)
        self.validate_deadline(deadline)
