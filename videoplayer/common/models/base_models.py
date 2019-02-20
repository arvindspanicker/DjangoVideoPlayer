# Python imports
import uuid

# Django imports
from django.db import models

# Custom imports
from .managers import ActiveObjectsManager, InactiveObjectsManager

# Create your models here.
class BaseModel(models.Model):
    """
    Every model class should extend this class.
    Here we will implement all the logic we want to be present in every model.
    """
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    STATUS_STYLE_ACTIVE = 'success'
    STATUS_STYLE_INACTIVE = 'danger'

    uid = models.UUIDField(db_index=True, primary_key=False, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')
    active = models.BooleanField(db_index=True, default=True, verbose_name='active')

    class Meta:
        abstract = True

    # MANAGERS
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    inactive_objects = InactiveObjectsManager()

    def __str__(self):
        return str(self.uid)

    @property
    def get_uid(self):
        return str(self.uid)

    # METHODS
    def delete(self):
        """
        Implements logical delete
        """
        if self.active:
            self.active = False
            self.save()
            return True
        else:
            return False

    def undelete(self):
        """
        Implements logical undelete
        """
        if not self.active:
            self.active = True
            self.save()
            return True
        else:
            return False

    @property
    def get_status_as_string(self):
        return self.STATUS_ACTIVE if self.active else self.STATUS_INACTIVE

    @property
    def get_status_style_as_string(self):
        return self.STATUS_STYLE_ACTIVE if self.active else self.STATUS_STYLE_INACTIVE
