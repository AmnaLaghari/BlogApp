from django.test import TestCase, Client
from UserApp.factories import UserFactory, GroupFactory, user_password
from django.urls import reverse
from PostApp.factories import PostFactory
from CommentsApp.factories import CommentFactory
from CommentsApp.forms import CommentForm


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        group_user = GroupFactory.create()
        moderator_group = GroupFactory.create(name='moderator')
        self.user = UserFactory.create(groups=(group_user,))
        self.moderator = UserFactory.create(groups=(moderator_group,))
        self.post1 = PostFactory.create(author=self.user)
        self.form_data = {
            'body': 'this is my test comment',
            'commentor': self.user,
            'post': self.post1,
        }
        self.comment = CommentFactory.create(
            post=self.post1, commentor=self.user)

    def test_add_comment_GET(self):
        form = CommentForm(data=self.form_data)
        self.client.login(username=self.user.username, password=user_password)
        response = self.client.get(
            reverse('add_comment', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comment/add_comment.html')
        self.assertTrue(form.is_valid())

    def test_add_comment_POST(self):
        form = CommentForm(data=self.form_data)
        self.client.login(username=self.user.username, password=user_password)
        response = self.client.post(
            reverse('add_comment', kwargs={'pk': self.post1.id}), {'body': 'test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,  reverse(
            'post_detail', kwargs={'pk': self.post1.id}))
        self.assertTrue(form.is_valid())

    def test_delete_comment_POST(self):
        self.client.login(username=self.moderator.username,
                          password=user_password)
        response = self.client.delete(
            reverse('delete_comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/posts/index/')

    def test_delete_comment_if_reported(self):
        self.client.login(username=self.moderator.username,
                          password=user_password)
        self.comment.reported = True
        self.comment.save()
        response = self.client.delete(
            reverse('delete_comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/posts/index/')
