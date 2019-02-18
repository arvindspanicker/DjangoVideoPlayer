from common.models import BaseModel as CommonBaseModel

class BaseModel(CommonBaseModel):

    # NOTE: all derived models will have a customer field, even if it is redundant, to speed up queries
    class Meta:
        abstract = True

