from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
class PostListView(ListView):
  model = Post
  template_name= 'post/post_list.html'

class PostDetailView(DetailView):
  model = Post
  template_name= 'post/post_details.html'

class AddPostView(CreateView):
  model = Post
  template_name = 'post/add_post.html'
  form_class= PostForm

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super(AddPostView, self).form_valid(form)

class UpdatePostView(UpdateView):
  model= Post
  template_name = 'post/edit_post.html'
  form_class= PostForm

class DeletePostView(DeleteView):
  model = Post
  template_name= 'post/delete_post.html'
  success_url = reverse_lazy('posts')
