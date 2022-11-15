from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from .decorators import allowed_users
from django.utils.decorators import method_decorator
from UserApp.templatetags import poll_extras
@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class PostListView(ListView):
  model = Post
  template_name= 'post/post_list.html'

@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class PostDetailView(DetailView):
  model = Post
  template_name= 'post/post_details.html'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.status == 'pending':
      messages.error(request, "This post is send for approval")
      return redirect('posts')
    return super().dispatch(request, *args, **kwargs)

@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
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

  @method_decorator(allowed_users(allowed_roles=['user','admin']))
  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.author != self.request.user and self.request.user.groups.all()[0].name != 'admin':
        messages.error(request, "you are not authorized to edit this post")
        raise Http404("You are not allowed to edit this Post")
    return super(UpdatePostView, self).dispatch(request, *args, **kwargs)

class DeletePostView(DeleteView):
  model = Post
  template_name= 'post/delete_post.html'
  success_url = reverse_lazy('posts')

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.author != self.request.user  and self.request.user.groups.all()[0].name != 'admin':
      messages.error(request, "you are not authorized to delete this post")
      raise Http404("You are not allowed to delete this Post")
    return super(DeletePostView, self).dispatch(request, *args, **kwargs)

@allowed_users(allowed_roles=['moderator'])
def index(request):
  posts = Post.objects.all()
  context = {'posts': posts}
  return render(request, 'UserApp/index.html', context=context)

@allowed_users(allowed_roles=['moderator'])
def approval(request,pk):
  post = Post.objects.get(pk=pk)
  post.status = 'approved'
  post.save()
  return redirect('index')

def handler404(request, exception):
  return render(request, '404.html')
