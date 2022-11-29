import threading
import time

import requests
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import UpdateView

from blog_app import settings

from . import models
from .decorators import unauthenticated_user
from .forms import SigninForm, SignupForm, UpdateUserForm
from .tokens import generate_token
from .utils import is_moderator


# from lockout.exceptions import LockedOut
def home(request):
    if request.user.is_authenticated:
        if is_moderator(request.user):
            return redirect('index')
        return redirect('posts')
    return render(request, 'UserApp/home.html')


def signout(request):
    logout(request)
    messages.success(request, "you have logged out successfully")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = models.CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


class Signup(View):
    def check_user(self, form_username):
        user_length = models.CustomUser.objects.filter(
            username=form_username).count()
        if user_length > 0:
            messages.error(self.request, 'Username already exists')
            return False
        return True

    def check_password(self, password, confirm_password):
        if len(password) < 6:
            messages.error(
                self.request, 'Password must be at least 6 characters')
            return False
        else:
            if password != confirm_password:
                messages.error(
                    self.request, 'Password does not match confirm_password')
                return False
            return True

    def get(self, request):
        context = {'form': SignupForm()}
        return render(request, 'UserApp/signup.html', context)

    def post(self, request):
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        group = request.POST.get('groups')
        email_check = self.check_user(username)
        password_check = self.check_password(password, confirm_password)
        if email_check and password_check:
            myuser = models.CustomUser.objects.create_user(
                username=username, email=email, password=password, first_name=firstname, last_name=lastname)
            myuser.groups.add(group)
            myuser.is_active = False
            myuser.save()
            current_site = get_current_site(request)
            subject = "Confirmation email"
            message = render_to_string('confirmation_email.html', {
                'name': myuser.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                subject, message, settings.EMAIL_HOST_USER, [myuser.email])
            email.fail_silently = True
            email.send()
            messages.success(
                request, "Your account has been successfully created")
            return redirect('signin')
        else:
            return redirect('signup')


@method_decorator(unauthenticated_user, name='dispatch')
class Signin(View):

    def locked_out(self, request):
        request.session.flush()
        messages.success(request, "Your account has been unlocked.")
        render(request, 'UserApp/signin.html')


    def get(self, request):
        context = {'form': SigninForm()}
        return render(request, 'UserApp/signin.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully")
            if is_moderator(request.user):
                return redirect('index')
            return redirect('posts')
        else:
            messages.error(request, "Bad credentials")
            if request.session.get('count', 0) == 0:
                request.session['count'] = 1
            else:
                request.session['count'] += 1
                if request.session['count'] == 5:
                    timer = threading.Timer(
                        10.0, self.locked_out, args=[request])
                    timer.start()
                    messages.error(
                        request, "You cannot signin now, you account is locked.")

            return redirect('signin')


class UpdateUser(UpdateView):
    form_class = UpdateUserForm
    template_name = 'UserApp/edit.html'
    success_url = reverse_lazy('posts')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        myuser = self.request.user
        myuser.is_active = False
        logout(self.request)
        messages.success(
            self.request, 'User updated successfully kindly login again')
        current_site = get_current_site(self.request)
        subject = "Confirmation email"
        message = render_to_string('confirmation_email.html', {
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            subject, message, settings.EMAIL_HOST_USER, [myuser.email])
        email.fail_silently = True
        email.send()
        return super(UpdateUser, self).form_valid(form)
