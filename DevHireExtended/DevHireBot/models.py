from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB in bytes
    if value.size > limit:
        raise ValidationError('File size cannot exceed 5 MB.')

class User(AbstractUser):
    email = models.EmailField(unique=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ]
    )
    
   