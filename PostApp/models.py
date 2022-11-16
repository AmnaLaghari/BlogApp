from django.db import models
from UserApp.models import CustomUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from datetime import datetime, date

class Post(models.Model):
  title = models.CharField(max_length=255)
  content = RichTextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  reported = models.BooleanField(default=False)
  status = models.CharField(max_length=255, default='pending')
  post_date = models.DateField(auto_now_add=True)
  likes = models.ManyToManyField(CustomUser, related_name='blog_posts')

  def get_absolute_url(self):
    return reverse('post_detail', args=[self.id])

