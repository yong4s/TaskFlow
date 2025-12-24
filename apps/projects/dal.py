from typing import TYPE_CHECKING

from django.apps import apps
from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import Prefetch
from django.db.models import QuerySet
from django.db.models import When

from apps.projects.models import Project
from apps.utils.dal import BaseRepository

if TYPE_CHECKING:
    from apps.accounts.models import User


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def get_by_user(self, user: 'User') -> QuerySet:
        return self.filter_by(user=user)

    def get_by_user_with_tasks(self, user: 'User') -> QuerySet:
        """Get projects with tasks prefetched and sorted."""
        Task = apps.get_model('tasks', 'Task')

        tasks_prefetch = Prefetch(
            'tasks',
            queryset=Task.objects.order_by(
                Case(When(status='done', then=1), default=0, output_field=IntegerField()), '-priority', '-created_at'
            ),
        )

        return self.filter_by(user=user).prefetch_related(tasks_prefetch).order_by('-created_at')

    def get_by_name(self, name: str, user: 'User') -> QuerySet:
        return self.filter_by(name__icontains=name, user=user)
