import factory
from .models import Post
from faker import Faker

fake = Faker()

class PostFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Post

  title = fake.name()
  content = fake.text()
  reported = False
  status = 'approved'
  post_date = fake.date()
  like_count = 0
