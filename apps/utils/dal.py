"""Base repository implementing the Repository pattern for data access."""
from abc import ABC
from typing import Any

from django.db import models
from django.db.models import QuerySet

from apps.utils.decorators import handle_dal_exceptions


class BaseRepository(ABC):
    """
    Base repository class providing common CRUD operations for Django models.

    This class follows the Repository pattern and provides database
    access with automatic error handling.
    """

    def __init__(self, model):
        self.model = model

    @handle_dal_exceptions
    def get_by_id(self, obj_id: int) -> models.Model:
        """Get a single object by its ID."""
        return self.model.objects.get(id=obj_id)

    def get_all(self) -> QuerySet:
        """Get all objects."""
        return self.model.objects.all()

    def filter_by(self, **kwargs: Any) -> QuerySet:
        """Filter objects by given criteria."""
        return self.model.objects.filter(**kwargs)

    @handle_dal_exceptions
    def create(self, **kwargs: Any) -> models.Model:
        """Create a new object."""
        return self.model.objects.create(**kwargs)

    @handle_dal_exceptions
    def update(self, instance: models.Model, **kwargs: Any) -> models.Model:
        """Update an existing object."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: models.Model) -> None:
        """Delete an object."""
        instance.delete()

    def exists(self, **kwargs: Any) -> bool:
        """Check if objects matching the given criteria exist."""
        return self.model.objects.filter(**kwargs).exists()
