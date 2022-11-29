from django.test import TestCase, Client
from django.urls import reverse
from UserApp.models import CustomUser
from django.contrib.auth import get_user
from django.contrib.auth.models import Group
from UserApp.factories import UserFactory, GroupFactory, user_password
import factory
from faker import Faker

fake = Faker()


class TestViews(TestCase):

    def setUp(self):
        self.group = GroupFactory.create()
        self.moderator_group = GroupFactory.create(name='moderator')

        self.client = Client()
        self.user = UserFactory.create(groups=(self.group,))
        self.moderator = UserFactory.create(groups=(self.moderator_group,))

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserApp/home.html')

    def test_signout_GET(self):
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_signin_GET(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserApp/signin.html')

    def test_signin_success_POST(self):
        response = self.client.post(
            reverse('signin'), {'username': self.user.username, 'password': user_password}, format='text/html')
        self.client.login(username=self.user.username, password=user_password)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/posts/')

    def test_signin_success_if_moderator_POST(self):
        response = self.client.post(
            reverse('signin'), {'username': self.moderator.username, 'password': user_password}, format='text/html')
        self.client.login(username=self.user.username, password=user_password)
        self.assertEqual(response.status_code, 302)

    def test_signin_lockedout(self):
        for i in range(0, 5):
            response = self.client.post(
                reverse('signin'), {'username': self.moderator.username, 'password': 1111111}, format='text/html')
            self.client.login(username=self.user.username, password=1111111)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin/')

    def test_signup_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserApp/signup.html')

    def test_cannot_signup_username_already_exist_POST(self):
        data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password,
            'confirm_password': 'wrongpassword',
            'groups': self.user.groups
        }
        response = self.client.post(
            reverse('signup'), data, format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/')

    def test_cannot_signup_password_wrong_length_POST(self):
        data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': 1,
            'confirm_password': 1,
            'groups': self.user.groups
        }
        response = self.client.post(
            reverse('signup'), data, format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/')

    def test_signup_success_POST(self):
        data = {
            'username': fake.name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': user_password,
            'confirm_password': user_password,
            'groups': self.user.groups.all()[0].id
        }
        response = self.client.post(
            reverse('signup'), data, format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin/')


    # def test_signup_success_POST(self):
    #     data = {
    #         'username': fake.name(),
    #         'first_name': fake.first_name(),
    #         'last_name': fake.last_name(),
    #         'email': fake.email(),
    #         'password': user_password,
    #         'confirm_password': user_password,
    #         'groups': (self.group.id,)
    #     }
    #     response = self.client.post(
    #         reverse('signup'), data, format='text/html')
    #     user = UserFactory.create(
    #         username=data['username'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=data['password'])
    #     user.save()
    #     user.groups.set(data['groups'])
    #     user.save()
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/signin/')
    #     # print('singin success')
