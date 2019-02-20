# Django imports
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Custom imports
from .base import BaseModel


class UserModel(BaseModel, AbstractUser):
    """
    Extended User model.
    Add Additional profile features  here
    """
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def get_name(self):
        name = self.get_full_name
        if not (self.first_name or self.last_name):
            name = self.username

        return name
