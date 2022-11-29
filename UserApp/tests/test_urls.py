from django.test import SimpleTestCase
from django.urls import reverse, resolve
from UserApp.views import *


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_signin_url_is_resolved(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func.view_class, Signin)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, Signup)

    def test_edit_user_url_is_resolved(self):
        url = reverse('edit_user')
        self.assertEqual(resolve(url).func.view_class, UpdateUser)

    def test_signout_url_is_resolved(self):
        url = reverse('signout')
        self.assertEqual(resolve(url).func, signout)
