from django.shortcuts import render
from PostApp.decorators import allowed_users
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .models import Suggestion
from django.urls import reverse_lazy
from PostApp.models import Post
from .forms import SuggestionForm

@method_decorator(allowed_users(allowed_roles=['user','admin']), name='dispatch')
class AddSuggestionView(CreateView):
  model = Suggestion
  template_name = 'suggestion/add_suggestion.html'
  form_class= SuggestionForm
  reverse_lazy('posts')


  def form_valid(self, form):
    form.instance.suggestor = self.request.user
    form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
    return super(AddSuggestionView, self).form_valid(form)
