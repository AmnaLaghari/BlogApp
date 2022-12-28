from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views
from knox import views as knox_views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signin/', views.Signin.as_view(), name='signin'),
    path('edit_user/', views.UpdateUser.as_view(), name='edit_user'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
urlpatterns += staticfiles_urlpatterns()
