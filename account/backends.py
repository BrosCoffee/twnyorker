# from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, user_email=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == user_email)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = SiteUser.objects.get(user_email=user_email)
            except SiteUser.DoesNotExist:
                return None
            return user
        return None

    def get_user(self, user_id):
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None
