from django.shortcuts import redirect
from django.contrib import messages
from UserApp.utils import is_not_moderator

def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name
      if group in allowed_roles:
        return view_func(request, *args, **kwargs)
      else:
        if is_not_moderator(request.user):
          messages.error(request,'You are not authorized to perform this action')
          return redirect('posts')
        else:
          messages.error(request,'You are not authorized to perform this action')
          return redirect('index')
    return wrapper_func
  return decorator
