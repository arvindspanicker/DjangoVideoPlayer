# Custom imports
from common.models import BaseModel as CommonBaseModel

class BaseModel(CommonBaseModel):
    class Meta:
        abstract = True

