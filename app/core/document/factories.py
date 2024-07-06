import factory
from datetime import datetime
from factory.django import DjangoModelFactory
from django.contrib.contenttypes.models import ContentType
from .models import BimaCoreDocument
from common.enums.file_type import get_file_type_choices

class BimaCoreDocumentFactory(DjangoModelFactory):
    class Meta:
        model = BimaCoreDocument

    document_name = factory.Sequence(lambda n: f"Document {n}")
    description = "Test document"
    file_name = "test_document.pdf"
    file_content_type = "application/pdf"
    file_extension = ".pdf"
    date_file = datetime.now()
    file_path = factory.django.FileField(filename='test_document.pdf')
    file_type = factory.Iterator(get_file_type_choices(), getter=lambda c: c[0])
    is_favorite = False
    parent_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.parent_model))
    parent_id = factory.Sequence(lambda n: n)

    @classmethod
    def create_batch(cls, size, **kwargs):
        return [cls.create(**kwargs) for _ in range(size)]
