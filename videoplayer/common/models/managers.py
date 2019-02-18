from django.db import models


class ActiveObjectsManager(models.Manager):
    """
    This is a model manager which will return all objects with active=True.
    """
    def get_queryset(self):
        return super(ActiveObjectsManager, self).get_queryset().filter(active=True)


class InactiveObjectsManager(models.Manager):
    """
    This is a model manager which will return all objects with active=False.
    """
    def get_queryset(self):
        return super(InactiveObjectsManager, self).get_queryset().filter(active=False)
