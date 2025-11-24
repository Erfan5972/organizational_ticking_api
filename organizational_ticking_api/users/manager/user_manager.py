from django.contrib.auth.models import BaseUserManager as BUM
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BUM):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create a user with the given username and password.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields to be set on the user.
        Returns:
            User: The created user.
        Raises:
            ValueError: If the user does not have a username.
        """
        if not username:
            raise ValueError(_("field username is required."))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create a superuser with the given username and password.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields to be set on the user.
        Returns:
            User: The created superuser.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(username, password, **extra_fields)
