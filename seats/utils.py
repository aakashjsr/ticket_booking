from django.contrib.auth.models import User


def get_user(email, first_name):
    """
    Gets or creates a new user with the given email
    :param email: email of user
    :param first_name: first name of user
    :return: user object
    """
    user, _ = User.objects.get_or_create(username=email, defaults={
        "email": email,
        "first_name": first_name
    })
    return user
