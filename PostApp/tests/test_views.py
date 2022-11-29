from django.test import TestCase, Client
from UserApp.factories import UserFactory, GroupFactory, user_password
from django.urls import reverse
from PostApp.forms import PostForm
from PostApp.factories import PostFactory

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        group_user = GroupFactory.create()
        moderator_group = GroupFactory.create(name = 'moderator')
        self.user = UserFactory.create(groups=(group_user,))
        self.moderator = UserFactory.create(groups=(moderator_group,))
        self.form_data = {
            'title': 'Test post',
            'content': 'this is my test post',
            'author': self.user,
        }
        self.post1 = PostFactory.create(author = self.user)
        self.post2 = PostFactory.create(author = self.user, reported = True)
        self.user2 = UserFactory.create(groups=(group_user,))


    def test_add_post_view_GET(self):
        self.client.login(username= self.user.username, password= user_password)
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/add_post.html')

    def test_cannot_add_post_if_moderator(self):
        self.client.login(username= self.moderator.username, password= user_password)
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/posts/index/')

    def test_add_post_view_POST(self):
        form = PostForm(data=self.form_data)
        self.client.login(username= self.user.username, password= user_password)
        reponse = self.client.post(reverse('add_post'),{'title': 'test post', 'content': 'hey this is my test post'}, format='text/html')
        self.assertEqual(reponse.status_code, 302)
        self.assertTrue(form.is_valid())

    def test_delete_post_view_DELETE(self):
        self.client.login(username= self.user.username, password= user_password)
        post = self.post1
        response = self.client.delete(reverse('delete_post',kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/posts/')

    def test_delete_post_if_reported_DELETE(self):
        self.client.login(username= self.moderator.username, password= user_password)
        post = self.post2
        response = self.client.delete(reverse('delete_post',kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/posts/index/')

    def test_delete_post_if_moderator_DELETE(self):
        self.client.login(username= self.moderator.username, password= user_password)
        post = self.post1
        response = self.client.delete(reverse('delete_post',kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/posts/index/')

    def test_delete_post_if_not_creator(self):
        self.client.login(username= self.user2.username, password= user_password)
        post = self.post1
        response = self.client.delete(reverse('delete_post',kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code,200)

    def test_like_post_POST(self):
        self.client.login(username= self.user2.username, password= user_password)
        post = self.post1
        response = self.client.post(reverse('like_post'),{
            'postid': post.id
        })
        response = self.client.post(reverse('like_post'),{
            'postid': post.id
        })
        self.assertEqual(response.status_code,200)
