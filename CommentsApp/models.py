from django.db import models
from UserApp.models import CustomUser
from PostApp.models import Post
from ckeditor.fields import RichTextField
from django.urls import reverse


class Comment(models.Model):
  commentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name="comments" ,on_delete=models.CASCADE)
  body = RichTextField()
  reported = models.BooleanField(default=False)
  date_added = models.DateField(auto_now_add=True)
  likes = models.ManyToManyField(CustomUser, related_name='comments_likes',blank=True, null=True)

  def get_absolute_url(self):
    return reverse('post_detail', kwargs={'pk':self.post.pk})
