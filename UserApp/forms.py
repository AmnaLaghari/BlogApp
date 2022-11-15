from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
  password=forms.CharField(widget=forms.PasswordInput())
  confirm_password=forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = CustomUser
    fields = ["email", "username", "password", "confirm_password", "first_name", "last_name", "groups"]

class SigninForm(forms.ModelForm):
  # password=forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = CustomUser
    fields = ["email", "password"]
