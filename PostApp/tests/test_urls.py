from django.test import SimpleTestCase
from django.urls import reverse, resolve
from PostApp.views import *


class TestUrls(SimpleTestCase):

    def test_add_post_url_is_resolved(self):
        url = reverse('add_post')
        self.assertEqual(resolve(url).func.view_class, AddPostView)

    def test_delete_post_url_is_resolved(self):
        url = reverse('delete_post', kwargs={"pk": 1234})
        self.assertEqual(resolve(url).func.view_class, DeletePostView)
