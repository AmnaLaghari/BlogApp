from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from .models import Post

# Create your views here.
class PostListView(ListView):
  model = Post
  template_name= 'post/post_list.html'

class PostDetailView(DetailView):
  model = Post
  template_name= 'post/post_details.html'

class AddPostView(CreateView):
  model = Post
  template_name = 'post/add_post.html'
  fields= '__all__'
