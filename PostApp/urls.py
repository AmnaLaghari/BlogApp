from django.contrib import admin
from django.urls import path
from .views import AddPostView, PostListView, PostDetailView, UpdatePostView, DeletePostView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(PostListView.as_view(), login_url='signin'), name='posts'),
    path('Add_post', login_required(AddPostView.as_view(), login_url='signin'), name='add_post'),
    path('<int:pk>', login_required(PostDetailView.as_view(), login_url='signin'), name='post_detail'),
    path('edit_post/<int:pk>', login_required(UpdatePostView.as_view(), login_url='signin'), name='update_post'),
    path('delete_post/<int:pk>', login_required(DeletePostView.as_view(), login_url='signin'), name='delete_post'),
]
