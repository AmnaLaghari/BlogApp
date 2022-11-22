from django.db import models
from django.urls import reverse

from PostApp.models import Post
from UserApp.models import CustomUser


class Suggestion(models.Model):
    suggestor = models.ForeignKey(
        CustomUser, related_name="suggestion", on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey(
        Post, related_name="suggestions", on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})


class Reply(models.Model):
    replier = models.ForeignKey(
        CustomUser, related_name="suggestion_replier", on_delete=models.CASCADE)
    suggestion = models.ForeignKey(
        Suggestion, related_name="replies", on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.suggestion.post.pk})
