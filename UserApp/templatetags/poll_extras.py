from django import template

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
