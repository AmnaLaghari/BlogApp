from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
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

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.author != self.request.user:
        messages.error(request, "you are not authorized to edit this post")
        raise Http404("You are not allowed to edit this Post")
    return super(UpdatePostView, self).dispatch(request, *args, **kwargs)

class DeletePostView(DeleteView):
  model = Post
  template_name= 'post/delete_post.html'
  success_url = reverse_lazy('posts')

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.author != self.request.user:
        messages.error(request, "you are not authorized to delete this post")
        raise Http404("You are not allowed to delete this Post")
    return super(DeletePostView, self).dispatch(request, *args, **kwargs)


def handler404(request, exception):
  return render(request, '404.html')
