from django.db import models
from UserApp.models import CustomUser
from PostApp.models import Post
from django.urls import reverse

class Suggestion(models.Model):
  suggestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  body = models.TextField()
  post = models.ForeignKey(Post, related_name="suggestions" ,on_delete=models.CASCADE)
  date_added = models.DateField(auto_now_add=True)

  def get_absolute_url(self):
    return reverse('post_detail', kwargs={'pk':self.post.pk})
