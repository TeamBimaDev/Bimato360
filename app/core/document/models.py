import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from core.abstract.models import AbstractModel
from common.enums.file_type import get_file_type_choices
from rest_framework import status
from rest_framework.exceptions import ValidationError


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
        ordering = ['-created', 'file_name']
        permissions = []


def create_document_from_parent_entity(data_document_to_save, parent):
    for document_data in data_document_to_save:
        create_single_document(document_data, parent)


def create_single_document(document_data, parent):
    try:
        BimaCoreDocument.objects.create(
            document_name=document_data.get('document_name', ''),
            description=document_data.get('description', ''),
            date_file=document_data.get('date_file', ''),
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id
        )
        return True
    except ValidationError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def get_documents_for_parent_entity(parent):
    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(parent),
        parent_id=parent.id
    )
