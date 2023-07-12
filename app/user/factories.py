import factory
from factory.django import DjangoModelFactory
from user.models import User
from faker import Faker
faker = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        self.password = faker.text(max_nb_chars=5)
        self.confirm_password = self.password