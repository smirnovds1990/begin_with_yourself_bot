import os

from django.core.exceptions import ValidationError

from .constants import VALID_VIDEO_EXTENSIONS


def validate_video_extension(value):

    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in VALID_VIDEO_EXTENSIONS:
        raise ValidationError('Неподдерживаемый формат файла.')
