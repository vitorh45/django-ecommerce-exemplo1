# coding: utf-8 
from django.conf import settings
from django.contrib.auth.models import User, check_password

class EmailBackend(object):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except:
            return None
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

