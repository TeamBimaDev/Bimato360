import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from core.abstract.models import AbstractModel
from common.enums.file_type import get_file_type_choices


class BimaCoreDocument(AbstractModel):
    def document_file_path(self, filename):
        ext = os.path.splitext(filename)[1]
        filename = f'{uuid.uuid4()}{ext}'
        self.file_name = filename
        self.file_extension = ext
        return os.path.join('uploads', 'documents', self.parent_type, filename)

    document_name = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=255)
    date_file = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to=document_file_path)
    file_type = models.CharField(max_length=100, choices=get_file_type_choices())
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

    def __str__(self) -> str:
        return self.file_name

    class Meta:
        ordering = ['-date_file', 'file_name']
        permissions = []


def create_document_from_parent_entity(data_document_to_save, parent):
    for document_data in data_document_to_save:
        BimaCoreDocument.objects.create(
            document_name=document_data.get('number', ''),
            description=document_data.get('street', ''),
            file_name=document_data.get('street2', ''),
            file_extension=document_data.get('zip', ''),
            date_file=document_data.get('city', ''),
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id
        )
