from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView

from PostApp.decorators import allowed_users
from PostApp.models import Post
from UserApp.utils import is_user

from .forms import ReplyForm, SuggestionForm
from .models import Reply, Suggestion


@method_decorator(allowed_users(allowed_roles=['user', 'admin']), name='dispatch')
class AddSuggestionView(CreateView):
    model = Suggestion
    template_name = 'suggestion/add_suggestion.html'
    form_class = SuggestionForm
    reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.suggestor = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super(AddSuggestionView, self).form_valid(form)


class DeleteSuggestionView(DeleteView):
    model = Suggestion
    template_name = 'suggestion/delete_suggestion.html'
    success_url = reverse_lazy('posts')

    @method_decorator(allowed_users(allowed_roles=['user']))
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if is_user(self.request.user):
            if self.request.user != obj.suggestor:
                messages.error(
                    request, "you are not authorized to reject this suggestion")
                return redirect('post_detail', self.post.id)
        return super(DeleteSuggestionView, self).dispatch(request, *args, **kwargs)


@method_decorator(allowed_users(allowed_roles=['user']), name='dispatch')
class AddReplyView(CreateView):
    model = Reply
    template_name = 'comment/add_reply.html'
    form_class = ReplyForm
    reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.replier = self.request.user
        form.instance.suggestion = Suggestion.objects.get(
            pk=self.kwargs.get('pk'))
        return super(AddReplyView, self).form_valid(form)
