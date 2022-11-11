from django.contrib import admin
from django.urls import path
from .views import AddPostView, PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('Add_post', AddPostView.as_view(), name='add_post'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
]
