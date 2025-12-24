from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import QuerySet
from django.db.models import When

from apps.tasks.models import Task
from apps.utils.dal import BaseRepository

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.projects.models import Project


class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(Task)

    def get_by_id(self, task_id: int):
        return self.model.objects.select_related('project', 'project__user').get(id=task_id)

    def get_by_user(self, user: 'User') -> QuerySet:
        return self.filter_by(
            project__user=user,
        ).select_related('project')

    def get_by_status(self, status: str) -> QuerySet:
        return self.filter_by(status=status).select_related('project')

    def get_by_project(self, project: 'Project') -> QuerySet:
        return self.filter_by(project=project)

    def get_by_deadline_before(self, date: datetime) -> QuerySet:
        return self.filter_by(deadline__lt=date).select_related('project')

    def get_by_priority(self, priority: int) -> QuerySet:
        return self.filter_by(priority=priority).select_related('project')

    def get_by_status_and_user(self, status: str, user: 'User') -> QuerySet:
        return self.filter_by(
            status=status,
            project__user=user,
        ).select_related('project')

    def get_by_priority_and_user(self, priority: int, user: 'User') -> QuerySet:
        return self.filter_by(
            priority=priority,
            project__user=user,
        ).select_related('project')

    def get_by_project_sorted(self, project: 'Project') -> QuerySet:
        """Get tasks sorted with active tasks by priority, done tasks at bottom."""
        return self.filter_by(project=project).order_by(
            Case(
                When(status='new', then=1),
                When(status='in_progress', then=2),
                When(status='done', then=3),
                output_field=IntegerField(),
            ),
            '-priority',
            '-created_at',
        )

    def count_by_project(self, project: 'Project') -> int:
        return self.filter_by(project=project).count()
