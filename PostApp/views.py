from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from CommentsApp.models import Comment
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.contrib import messages
from .decorators import allowed_users
from django.utils.decorators import method_decorator
from UserApp.utils import is_not_admin, is_not_moderator, not_creator, is_pending, is_moderator, not_reported, not_pending
from django.http import HttpResponseRedirect
@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class PostListView(ListView):
  model = Post
  template_name= 'post/post_list.html'
  ordering= ['post_date']

@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class PostDetailView(DetailView):
  model = Post
  template_name= 'post/post_details.html'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if is_pending(obj):
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
    if not_creator(self.request.user,obj) and is_not_admin(self.request.user):
        messages.error(request, "you are not authorized to edit this post")
        raise Http404("You are not allowed to edit this Post")
    return super(UpdatePostView, self).dispatch(request, *args, **kwargs)

class DeletePostView(DeleteView):
  model = Post
  template_name= 'post/delete_post.html'

  @method_decorator(allowed_users(allowed_roles=['user','admin','moderator']))
  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if not_creator(self.request.user,obj)  and is_not_admin(self.request.user) and is_not_moderator(self.request.user):
      messages.error(request, "you are not authorized to delete this post")
      raise Http404("You are not allowed to delete this Post")
    if is_moderator(self.request.user):
      if not_reported(obj) and not_pending(obj):
        messages.error(request, "you are not authorized to delete this post as it is not reported")
        return redirect('index')
    return super(DeletePostView, self).dispatch(request, *args, **kwargs)

  def get_success_url(self):
    if self.request.user.groups.all()[0].name == 'moderator':
      return reverse_lazy('index')
    else:
      return reverse_lazy('posts')

@allowed_users(allowed_roles=['moderator'])
def index(request):
  posts = Post.objects.all()
  comments = Comment.objects.all()
  context = {'posts': posts, 'comments': comments}
  return render(request, 'UserApp/index.html', context=context)


@allowed_users(allowed_roles=['moderator'])
def approval(request,pk):
  post = Post.objects.get(pk=pk)
  post.status = 'approved'
  post.save()
  return redirect('index')

@allowed_users(allowed_roles=['user','admin'])
def report(request,pk):
  post = Post.objects.get(pk=pk)
  post.reported = True
  post.save()
  messages.success(request, 'this post has been reported')
  return redirect('posts')

def handler404(request, exception):
  return render(request, '404.html')

@allowed_users(allowed_roles=['moderator'])
def keep(request,pk):
  post = Post.objects.get(pk=pk)
  post.reported = False
  post.save()
  messages.success(request, 'this post has been removed from reported posts')
  return redirect('index')

def LikeView(request,pk):
  post = get_object_or_404(Post, id=request.POST.get('post_id'))
  if post.likes.filter(id=request.user.id).exists():
    post.likes.remove(request.user)
  else:
    post.likes.add(request.user)
  return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))
