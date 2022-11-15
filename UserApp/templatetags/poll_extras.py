from django import template
from PostApp.models import Post

register = template.Library()
@register.filter(name='get_role')
def get_role(user):
  return user.groups.all()[0].name

@register.filter(name='is_admin')
def is_admin(user):
  return True if user.groups.all()[0].name == 'admin' else False

@register.filter(name='is_moderator')
def is_moderator(user):
  return True if user.groups.all()[0].name == 'moderator' else False

@register.filter(name='is_user')
def is_user(user):
  return True if user.groups.all()[0].name == 'user' else False

@register.filter(name='is_author_of_post')
def is_author_of_post(user, post):
  return True if user == post.author else False

@register.filter(name='is_reported')
def is_reported(post):
  return True if post.reported == True else False

@register.filter(name='is_approved')
def is_approved(post):
  return True if post.status == 'approved' else False

@register.filter(name='is_pending')
def is_pending(post):
  return True if post.status == 'pending' else False

@register.filter(name='is_not_admin')
def is_not_admin(user):
  return True if user.groups.all()[0].name != 'admin' else False

@register.filter(name='count_reported')
def count_reported(posts):
  count = 0
  for post in posts:
    if post.reported == True:
      count +=1
  return count

@register.filter(name='count_pending')
def count_pending(posts):
  count = 0
  for post in posts:
    if post.status == 'pending':
      count +=1
  return count

@register.filter(name='count_approved')
def count_approved(posts):
  count = 0
  for post in posts:
    if post.status == 'approved':
      count +=1
  return count
