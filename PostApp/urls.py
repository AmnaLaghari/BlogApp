from django.contrib import admin
from django.urls import path, include
from .views import AddPostView, PostListView, PostDetailView, UpdatePostView, DeletePostView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('index/', login_required(views.index, login_url='signin'), name='index'),
    path('approve/<int:pk>', login_required(views.approval, login_url='signin'), name='approval'),
    path('report/<int:pk>', login_required(views.report, login_url='signin'), name='report'),
    path('',login_required(PostListView.as_view(), login_url='signin'), name='posts'),
    path('Add_post', login_required(AddPostView.as_view(), login_url='signin'), name='add_post'),
    path('<int:pk>', login_required(PostDetailView.as_view(), login_url='signin'), name='post_detail'),
    path('edit_post/<int:pk>', login_required(UpdatePostView.as_view(), login_url='signin'), name='update_post'),
    path('delete_post/<int:pk>', login_required(DeletePostView.as_view(), login_url='signin'), name='delete_post'),
    path('keep_post/<int:pk>', login_required(views.keep, login_url='signin'), name='keep_post'),
    path('like/<int:pk>', login_required(views.LikeView, login_url='signin'), name='like_post'),
    path('',include('CommentsApp.urls')),
    path('',include('suggestion.urls')),
]
