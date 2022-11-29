from PostApp.factories import PostFactory
from django.test import TestCase
from UserApp.factories import UserFactory, GroupFactory, user_password
from faker import Faker
fake = Faker()


class TestCustomerModel(TestCase):

    def setUp(self):
        group_user = GroupFactory.create()
        self.user = UserFactory.create(groups=(group_user,))
        self.post1 = PostFactory.create(author = self.user)

    def test_str(self):
        title = fake.name()
        self.post1.title = title
        self.assertEqual(self.post1.__str__(), title)
