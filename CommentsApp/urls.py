from django.contrib import admin
from django.urls import path, include
from .views import AddCommentView
from django.contrib.auth.decorators import login_required
from . import views
from .views import DeleteCommentView, AddReplyView
urlpatterns = [
  path('<int:pk>/comments/add_comment', login_required(AddCommentView.as_view(), login_url='signin'), name='add_comment'),
  path('comments/<int:pk>/report/', login_required(views.report, login_url='signin'), name='report_comment'),
  path('comments/<int:pk>/delete_comment/', login_required(DeleteCommentView.as_view(), login_url='signin'), name='delete_comment'),
  path('keep_comment/<int:pk>', login_required(views.keep, login_url='signin'), name='keep_comment'),
  path('<int:pk>/comments/<int:pk_comment>/like', login_required(views.LikeView, login_url='signin'), name='like_comment'),
  path('<int:pk>/comments/<int:pk_comment>/reply', login_required(AddReplyView.as_view(), login_url='signin'), name='add_reply'),
]
