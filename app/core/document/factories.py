import factory
from .models import BimaCoreDocument
from common.enums.file_type import get_file_type_choices
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


class BimaCoreDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreDocument

    document_name = factory.Faker('word')
    description = factory.Faker('text')
    file_name = factory.Faker('file_name')
    file_content_type = 'application/octet-stream'
    file_extension = factory.Faker('file_extension')
    date_file = factory.Faker('date_time_this_decade')
    file_type = factory.Faker('random_element', elements=get_file_type_choices())
    is_favorite = factory.Faker('boolean')
    parent_type = None
    parent_id = None
    @classmethod
    def with_parent(cls, parent):
        return cls(parent_type=ContentType.objects.get_for_model(parent), parent_id=parent.id)
    @classmethod
    def _create_file(cls):
        content = b"File content"
        file_name = "example_file.txt"
        file = SimpleUploadedFile(file_name, content)
        return File(file)

    file_path = factory.LazyAttribute(lambda _: BimaCoreDocumentFactory._create_file())