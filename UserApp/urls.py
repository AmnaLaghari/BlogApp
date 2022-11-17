from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signin/', views.Signin.as_view(), name='signin'),
    path('edit_user/',views.UpdateUser.as_view(), name='edit_user'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
urlpatterns += staticfiles_urlpatterns()
