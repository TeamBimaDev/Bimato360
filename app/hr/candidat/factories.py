<<<<<<< HEAD
import factory
from .models import BimaHrCandidat



class BimaHrCandidatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrCandidat

    availability_days = factory.Faker('random_int', min=1, max=7)
    message = factory.Faker('text')
    
=======
import factory
from .models import BimaHrCandidat
from core.document.models import BimaCoreDocument
from django.contrib.contenttypes.models import ContentType




class BimaHrCandidatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrCandidat

    availability_days = factory.Faker('random_int', min=1, max=7)
    message = factory.Faker('text')
    

class BimaCoreDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreDocument

    document_name = factory.Faker('word')
    file_name = factory.Faker('file_name', extension='jpg')
    file_content_type = 'application/octet-stream'
    file_extension = 'jpg'
    file_type = 'CANDIDAT_CV'
    file_path = factory.django.FileField(filename='N0044410.jpg')
    is_favorite = False
    parent_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(BimaHrCandidat))
    parent_id = factory.LazyAttribute(lambda o: BimaHrCandidatFactory().id)

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        if not create:
            return

        if 'file_path' in kwargs:
            self.file_path = kwargs['file_path']
            self.save()
>>>>>>> origin/ma-branch
