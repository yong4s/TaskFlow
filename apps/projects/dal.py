from typing import TYPE_CHECKING
from django.db.models import QuerySet

from apps.utils.dal import BaseRepository
from .models import Project

if TYPE_CHECKING:
    from apps.accounts.models import User


class ProjectRepository(BaseRepository):
    """Repository for Project model with simple database access methods."""

    def __init__(self):
        super().__init__(Project)

    def get_by_user(self, user: 'User') -> QuerySet:
        """Get projects for a specific user."""
        return self.filter_by(user=user)

    def get_by_user_with_tasks(self, user: 'User') -> QuerySet:
        """Get projects with tasks prefetched."""
        return self.filter_by(user=user).prefetch_related('tasks')

    def get_by_name(self, name: str, user: 'User') -> QuerySet:
        """Get projects filtered by name."""
        return self.filter_by(name__icontains=name, user=user)