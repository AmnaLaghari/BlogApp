from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AddSuggestionView
urlpatterns = [
  path('<int:pk>/suggestion/add_suggestion', login_required(AddSuggestionView.as_view(), login_url='signin'), name='add_suggestion'),
]
