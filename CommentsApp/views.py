from django.shortcuts import render
from django.views.generic import CreateView
from PostApp.decorators import allowed_users
from django.utils.decorators import method_decorator
from .models import Comment
from django.contrib import messages
from .forms import CommentForm
from PostApp.models import Post
from django.urls import reverse_lazy

# Create your views here.
@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class AddCommentView(CreateView):
  model = Comment
  template_name = 'comment/add_comment.html'
  form_class= CommentForm
  reverse_lazy('posts')


  def form_valid(self, form):
    form.instance.commentor = self.request.user
    form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
    return super(AddCommentView, self).form_valid(form)
