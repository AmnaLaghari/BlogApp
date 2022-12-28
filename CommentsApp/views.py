from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView

from PostApp.decorators import allowed_users
from PostApp.models import Post
from UserApp.utils import is_moderator, not_reported

from .forms import CommentForm, ReplyForm
from .models import Comment, Reply
from rest_framework import viewsets
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication


@method_decorator(allowed_users(allowed_roles=['user', 'admin']), name='dispatch')
class AddCommentView(CreateView):
    model = Comment
    template_name = 'comment/add_comment.html'
    form_class = CommentForm
    reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.commentor = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super(AddCommentView, self).form_valid(form)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'comment/delete_comment.html'
    success_url = reverse_lazy('index')

    @method_decorator(allowed_users(allowed_roles=['user', 'admin', 'moderator']))
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if is_moderator(self.request.user):
            if not_reported(obj):
                messages.error(
                    request, "you are not authorized to delete this post as it is not reported")
                return redirect('index')
        return super(DeleteCommentView, self).dispatch(request, *args, **kwargs)


@method_decorator(allowed_users(allowed_roles=['user', 'admin']), name='dispatch')
class AddReplyView(CreateView):
    model = Reply
    template_name = 'comment/add_reply.html'
    form_class = ReplyForm
    reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.replier = self.request.user
        form.instance.comment = Comment.objects.get(
            pk=self.kwargs.get('pk_comment'))
        return super(AddReplyView, self).form_valid(form)


@allowed_users(allowed_roles=['user', 'admin'])
def report(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.reported = True
    comment.save()
    messages.success(request, 'this comment has been reported')
    return redirect('posts')


@allowed_users(allowed_roles=['moderator'])
def keep(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.reported = False
    comment.save()
    messages.success(
        request, 'this comment has been removed from reported comments')
    return redirect('index')


def LikeView(request, pk, pk_comment):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


class CommmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
