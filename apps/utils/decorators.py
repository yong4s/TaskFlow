from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from .exceptions import DALError, ObjectNotFoundError, ValidationError


def handle_dal_exceptions(func):
    """
    Decorator to handle Django ORM exceptions and translate to domain exceptions.
    
    Catches specific Django database exceptions and converts them to our
    domain-specific exceptions while preserving the original stacktrace.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ObjectDoesNotExist:
            # Extract identifier from method arguments
            identifier = args[0] if args else str(kwargs) if kwargs else 'object'
            raise ObjectNotFoundError(self.model.__name__, identifier) from None
        except IntegrityError as e:
            # Database constraint violations (unique, foreign key)
            raise ValidationError('database', str(e)) from e
        except DatabaseError as e:
            # General database errors (connection, syntax, etc.)
            raise DALError(f'Database error: {str(e)}') from e
    return wrapper
