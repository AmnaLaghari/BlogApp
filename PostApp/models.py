from datetime import date, datetime

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from UserApp.models import CustomUser

status_choices = (
    ('pending', 'pending'),
    ('approved', 'approved'),
)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reported = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255, choices=status_choices, default='pending')
    post_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='blog_posts', blank=True)
    like_count = models.BigIntegerField(default='0')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])
