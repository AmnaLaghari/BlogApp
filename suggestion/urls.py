from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AddSuggestionView, DeleteSuggestionView, AddReplyView
urlpatterns = [
  path('<int:pk>/suggestion/add_suggestion', login_required(AddSuggestionView.as_view(), login_url='signin'), name='add_suggestion'),
  path('suggestions/delete_suggestion/<int:pk>', login_required(DeleteSuggestionView.as_view(), login_url='signin'), name='delete_suggestion'),
  path('suggestions/reply_suggestion/<int:pk>', login_required(AddReplyView.as_view(), login_url='signin'), name='reply_suggestion'),
]

