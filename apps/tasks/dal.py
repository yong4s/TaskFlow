from typing import TYPE_CHECKING
from datetime import datetime
from django.db.models import QuerySet

from apps.utils.dal import BaseRepository
from .models import Task

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.models import Project


class TaskRepository(BaseRepository):
    """Repository for Task model with simple database access methods."""

    def __init__(self):
        super().__init__(Task)

    def get_by_user(self, user: 'User') -> QuerySet:
        """Get tasks for a specific user."""
        return self.filter_by(
            project__user=user,
        ).select_related('project')

    def get_by_status(self, status: str) -> QuerySet:
        """Get tasks filtered by status."""
        return self.filter_by(status=status).select_related('project')

    def get_by_project(self, project: 'Project') -> QuerySet:
        """Get all tasks for a specific project."""
        return self.filter_by(project=project)

    def get_by_deadline_before(self, date: datetime) -> QuerySet:
        """Get tasks with deadline before specified date."""
        return self.filter_by(deadline__lt=date).select_related('project')

    def get_by_priority(self, priority: int) -> QuerySet:
        """Get tasks filtered by priority."""
        return self.filter_by(priority=priority).select_related('project')

    def get_by_status_and_user(self, status: str, user: 'User') -> QuerySet:
        """Get tasks filtered by status and user."""
        return self.filter_by(
            status=status,
            project__user=user,
        ).select_related('project')

    def get_by_priority_and_user(self, priority: int, user: 'User') -> QuerySet:
        """Get tasks filtered by priority and user."""
        return self.filter_by(
            priority=priority,
            project__user=user,
        ).select_related('project')

