from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    email = models.EmailField(_('email address'), db_collation='case_insensitive', unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
