from django.conf import settings
from django.contrib.auth.models import User
from Comunication_LTD.models import NS_user


class UserAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user:
                return user
            else:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user:
                return user.name
        except User.DoesNotExist:
            return None