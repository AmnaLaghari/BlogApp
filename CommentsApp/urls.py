from django.contrib import admin
from django.urls import path, include
from .views import AddCommentView
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
  path('<int:pk>/add_comment', login_required(AddCommentView.as_view(), login_url='signin'), name='add_comment'),
]
