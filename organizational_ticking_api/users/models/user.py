from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from organizational_ticking_api.common.models import BaseModel
from organizational_ticking_api.users.manager.user_manager import BaseUserManager


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("username"),
        help_text="A unique identifier used for user login. Must be unique across all users.",
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("first name"),
        help_text="The user's given name. Used for personalization and identification.",
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("last name"),
        help_text="The user's family name or surname. Helps distinguish users with similar first names.",
    )

    date_joined = models.DateTimeField(
        default=now,
        verbose_name=_("date joined"),
        help_text="The date and time when the user account was created. Useful for tracking account age.",
        editable=False,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
        help_text="Indicates whether the user account is currently active and allowed to log in.",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("is staff"),
        help_text="Designates whether the user has staff privileges, granting access to administrative features.",
    )

    objects = BaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @property
    def full_name(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.username
        )

    def __str__(self):
        """
        Return the username of the user.
        """
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
