from django import forms

from .models import Reply, Suggestion


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['body']


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['body']
