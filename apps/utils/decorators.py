import logging
from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db import IntegrityError

from apps.utils.exceptions import DALError
from apps.utils.exceptions import ObjectNotFoundError
from apps.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


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
            logger.exception('Database constraint violation in %s', func.__name__)
            error_field = 'database'
            error_message = str(e)
            raise ValidationError(error_field, error_message) from e
        except DatabaseError as e:
            # General database errors (connection, syntax, etc.)
            logger.exception('Database error in %s', func.__name__)
            error_message = f'Database error: {e!s}'
            raise DALError(error_message) from e

    return wrapper
