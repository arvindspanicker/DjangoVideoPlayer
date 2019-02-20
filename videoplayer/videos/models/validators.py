# Python imports
import os

# Django imports
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """
    Function that validates the extension of the uploaded video
    :param value: complete path including the filename
    :return: raises Validation error if not present in the valid extensions
    """
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.webm', '.mp4', '.mpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
