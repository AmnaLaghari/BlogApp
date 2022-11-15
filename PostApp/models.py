from django.db import models
from UserApp.models import CustomUser
from django.urls import reverse
from ckeditor.fields import RichTextField

class Post(models.Model):
  title = models.CharField(max_length=255)
  content = RichTextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  reported = models.BooleanField(default=False)
  status = models.CharField(max_length=255, default='pending')


  def get_absolute_url(self):
    return reverse('post_detail', args=[self.id])

