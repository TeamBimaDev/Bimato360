from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os
import uuid
from django.apps import apps


from core.abstract.models import AbstractModel


class BimaCoreDocument(AbstractModel):
    def document_file_path(instance, filename):

        """Generate file path for new recipe image."""
        ext = os.path.splitext(filename)[1]
        filename = f'{uuid.uuid4()}{ext}'
        instance.file_name = filename
        instance.file_extension = ext
        print(ext)
        print(filename)
        return os.path.join('uploads', 'documents',filename )


    LIST_TYPE_CV = 'CV'
    LIST_TYPE_RESUME = 'RESUME'
    LIST_TYPE_DRIVER_LICENCE = 'DRIVER_LICENCE'
    LIST_TYPE_PICTURE = 'PICTURE'

    LIST_TYPE_CHOICES = [
        (LIST_TYPE_CV, 'CV'),
        (LIST_TYPE_RESUME, 'RESUME'),
        (LIST_TYPE_DRIVER_LICENCE, 'DRIVER_LICENCE'),
        (LIST_TYPE_PICTURE, 'PICTURE'),
    ]
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label__in': [
                app_config.label for app_config in apps.get_app_configs()
                if app_config.label not in ['admin', 'auth', 'contenttypes', 'sessions', 'auditlog']
            ]
        }
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')
    document_name = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=255)
    date_file = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to=document_file_path)
    file_type = models.CharField(max_length=100, choices=LIST_TYPE_CHOICES)


    def __str__(self) -> str:
        return self.file_name

    class Meta:
        ordering = ['file_name']
        permissions = []

