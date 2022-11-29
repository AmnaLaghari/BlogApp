from django.test import SimpleTestCase
from django.urls import reverse, resolve
from CommentsApp.views import *


class TestUrls(SimpleTestCase):

    def test_add_post_url_is_resolved(self):
        url = reverse('add_comment',kwargs={"pk": 1234})
        self.assertEqual(resolve(url).func.view_class, AddCommentView)

    def test_delete_post_url_is_resolved(self):
        url = reverse('delete_comment', kwargs={"pk": 1234})
        self.assertEqual(resolve(url).func.view_class, DeleteCommentView)
