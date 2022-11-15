from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog_app import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.views import View
from django.utils.decorators import method_decorator
from . import models
from .decorators import unauthenticated_user
from .forms import SignupForm, SigninForm
from .utils import is_moderator

def home(request):
  return render(request, 'UserApp/home.html')

def signout(request):
  logout(request)
  messages.success(request, "you have logged out successfully")
  return redirect('home')

def activate(request, uidb64, token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    myuser = models.CustomUser.objects.get(pk = uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    myuser = None

  if myuser is not None and generate_token.check_token(myuser, token):
    myuser.is_active = True
    myuser.save()
    return redirect('home')
  else:
    return render(request, 'activation_failed.html')

class Signup(View):
  def get(self, request):
    context = {'form': SignupForm()}
    return render(request, 'UserApp/signup.html', context)

  def post(self,request):
    username  = request.POST['username']
    firstname  = request.POST['first_name']
    lastname  = request.POST['last_name']
    email  = request.POST['email']
    password  = request.POST['password']
    confirm_password  = request.POST['confirm_password']
    group = request.POST['groups']

    if password != confirm_password:
      messages.error(request,'Passowrd didnt match')
      return redirect('home')

    myuser = models.CustomUser.objects.create_user(username=username, email=email, password=password, first_name = firstname, last_name = lastname)
    myuser.groups.set(group)
    myuser.is_active = False
    myuser.save()

    current_site = get_current_site(request)
    subject = "Confirmation email"
    message = render_to_string('confirmation_email.html',{
      'name': myuser.username,
      'domain': current_site.domain,
      'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
      'token': generate_token.make_token(myuser)
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [myuser.email])
    email.fail_silently = True
    email.send()

    messages.success(request, "Your account has been successfully created")
    return redirect('signin')

@method_decorator(unauthenticated_user, name='dispatch')
class Signin(View):

  def get(self, request):
    context = {'form': SigninForm()}
    return render(request, 'UserApp/signin.html', context)

  def post(self, request):
    username  = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username = username, password = password)

    if user is not None:
      login(request,user)
      messages.error(request, "You have logged in successfully")
      if is_moderator(request.user):
        return redirect('index')
      return redirect('posts')
    else:
      messages.error(request, "Bad credentials")
      return redirect('home')

