from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'
    
    class Priority(models.IntegerChoices):
        VERY_LOW = 1, 'Very Low'
        LOW = 2, 'Low'
        MEDIUM = 3, 'Medium'
        HIGH = 4, 'High'
        VERY_HIGH = 5, 'Very High'

    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    deadline = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'tasks_task'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status', '-created_at'], name='idx_tasks_project_status_created'),
            models.Index(fields=['deadline'], name='idx_tasks_deadline', condition=models.Q(deadline__isnull=False)),
            models.Index(fields=['deadline', 'status'], name='idx_tasks_deadline_status', condition=models.Q(deadline__isnull=False)),
            models.Index(fields=['-updated_at'], name='idx_tasks_updated'),
        ]

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'
