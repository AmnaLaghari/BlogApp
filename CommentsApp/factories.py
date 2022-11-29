import factory
from .models import Comment
from faker import Faker

fake = Faker()

class CommentFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Comment

  body = fake.text()
  reported = False
  date_added = fake.date()
