from django import forms
from .models import CustomUser
from django.contrib.auth.models import Group

class SignupForm(forms.ModelForm):
  password=forms.CharField(widget=forms.PasswordInput())
  confirm_password=forms.CharField(widget=forms.PasswordInput())
  groups = forms.ModelChoiceField(queryset=Group.objects.all().exclude(name = 'admin'),
                                   required=True)

  class Meta:
    model = CustomUser
    fields = ["email", "username", "password", "confirm_password", "first_name", "last_name", "groups"]

class SigninForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ["email", "password"]

class UpdateUserForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email']
