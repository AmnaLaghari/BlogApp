from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
  username = models.CharField(_('Username'), max_length=255, unique=True)
  email = models.EmailField(_('Email'), max_length=255, unique=True)

  User = 1
  Moderator = 2

  Role = {
    (User, 'User'),
    (Moderator, 'Moderator'),
  }

  role = models.PositiveSmallIntegerField(choices=Role, blank=True, null=True)

