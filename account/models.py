from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime
import math

class SiteUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class SiteUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = SiteUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def age(self, selected_datetime_obj=None):
        # selected_datetime_obj allow users to enter any designated date
        today = selected_datetime_obj if selected_datetime_obj else datetime.now()
        date_of_birth = datetime.strptime(str(self.date_of_birth), '%Y-%m-%d')
        age = math.floor((today - date_of_birth).days/ 365.2425)
        return age

    def is_under_age(self, selected_datetime_obj=None, age=18):
        return True if self.age(selected_datetime_obj) < age else False

    @property
    def is_staff(self):
        return self.is_admin
