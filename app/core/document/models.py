import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
        app_label = self.parent_type.model
        return os.path.join('uploads', 'documents', app_label, filename)

    document_name = models.CharField(max_length=256, blank=False, null=False, default='new_document')
    description = models.TextField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=False, null=False)
    file_content_type = models.CharField(max_length=255, blank=False, null=False, default='application/octet-stream')
    file_extension = models.CharField(max_length=16, blank=False, null=False)
    date_file = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to=document_file_path)
    file_type = models.CharField(max_length=128,
                                 choices=get_file_type_choices())
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self) -> str:
        return self.file_name

    class Meta:
        ordering = ['-created', 'file_name']
        permissions = []

    @classmethod
    def create_document_for_partner(cls, parent, document_data):
        try:
            file = document_data['file_path']
            ext = os.path.splitext(file.name)[1]
            filename = f'{uuid.uuid4()}{ext}'
            file_content_type = file.content_type
            app_label = parent._meta.label

            if not file_content_type:
                raise ValidationError('Invalid file content type.')

            document = cls(
                document_name=document_data['document_name'],
                description=document_data['description'],
                date_file=document_data['date_file'],
                file_type=document_data['file_type'],
                file_content_type=file_content_type,
                parent_type=ContentType.objects.get_for_model(parent),
                parent_id=parent.id,
                file_name=filename,
                file_extension=ext
            )
            document.file_path.save(os.path.join('uploads', 'documents', app_label, filename), file)
            document.save()
            return True

        except ValidationError as e:
            return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}

        except Exception as e:
            return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def create_document_from_parent_entity(data_document_to_save, parent):
    for document_data in data_document_to_save:
        create_single_document(document_data, parent)


def create_single_document(document_data, parent):
    try:
        item = BimaCoreDocument.objects.create(
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
