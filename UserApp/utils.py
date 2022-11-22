def is_not_admin(user):
    return True if user.groups.all()[0].name != 'admin' else False


def is_not_moderator(user):
    return True if user.groups.all()[0].name != 'moderator' else False


def not_creator(user, post):
    return True if post.author != user else False


def is_pending(post):
    return True if post.status == 'pending' else False


def is_moderator(user):
    return True if user.groups.all()[0].name == 'moderator' else False


def is_user(user):
    return True if user.groups.all()[0].name == 'user' else False


def not_reported(post):
    return True if post.reported != True else False


def not_pending(post):
    return True if post.status != 'pending' else False
