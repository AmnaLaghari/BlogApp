import factory
from .models import CustomUser
import django.contrib.auth.models as auth_models
from django.contrib.auth.hashers import make_password


user_password = 'password'

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth_models.Group

    name = 'user'

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username =factory.Faker('name')
    password = make_password(user_password)
    email = factory.Faker('email')
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
