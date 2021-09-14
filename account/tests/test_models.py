from django.test import TestCase
from ..models import *
from datetime import datetime

class SiteUserTest(TestCase):
    def setUp(self):
        SiteUser.objects.create(email='testing01@gmail.com', first_name='Joe', last_name='Smith', date_of_birth='2000-04-05', is_admin=True)
        SiteUser.objects.create(email='testing02@gmail.com', first_name='Tina', last_name='Green', date_of_birth='2015-03-15')
        SiteUser.objects.create(email='testing03@gmail.com', first_name='Mark', last_name='White', date_of_birth='2008-06-26')
        SiteUser.objects.create(email='testing04@gmail.com', first_name='Peter', last_name='Griffin', date_of_birth='1990-07-07')

    def test_superuser(self):
        joe = SiteUser.objects.get(email='testing01@gmail.com')
        tina = SiteUser.objects.get(email='testing02@gmail.com')
        mark = SiteUser.objects.get(email='testing03@gmail.com')
        peter = SiteUser.objects.get(email='testing04@gmail.com')
        self.assertIs(joe.is_staff, True)
        self.assertIs(tina.is_staff, False)
        self.assertIs(mark.is_staff, False)
        self.assertIs(peter.is_staff, False)

    def test_age(self):
        joe = SiteUser.objects.get(email='testing01@gmail.com')
        tina = SiteUser.objects.get(email='testing02@gmail.com')
        mark = SiteUser.objects.get(email='testing03@gmail.com')
        peter = SiteUser.objects.get(email='testing04@gmail.com')
        datetime_obj = datetime.strptime('2026-03-14', '%Y-%m-%d')
        self.assertEqual(joe.age(datetime_obj), 25)   # 25 yr
        self.assertEqual(tina.age(datetime_obj), 10)  # 10 yr
        self.assertEqual(mark.age(datetime_obj), 17)  # 17 yr
        self.assertEqual(peter.age(datetime_obj), 35) # 35 yr

    def test_is_under_age(self):
        joe = SiteUser.objects.get(email='testing01@gmail.com')
        tina = SiteUser.objects.get(email='testing02@gmail.com')
        mark = SiteUser.objects.get(email='testing03@gmail.com')
        peter = SiteUser.objects.get(email='testing04@gmail.com')
        datetime_obj = datetime.strptime('2026-03-14', '%Y-%m-%d')
        # Under default age 18
        self.assertIs(joe.is_under_age(datetime_obj), False)   # 25 yr
        self.assertIs(tina.is_under_age(datetime_obj), True)   # 10 yr
        self.assertIs(mark.is_under_age(datetime_obj), True)   # 17 yr
        self.assertIs(peter.is_under_age(datetime_obj), False) # 35 yr
        # Under designated age 26
        self.assertIs(joe.is_under_age(datetime_obj, 16), False)   # 25 yr
        self.assertIs(tina.is_under_age(datetime_obj, 16), True)   # 10 yr
        self.assertIs(mark.is_under_age(datetime_obj, 16), False)   # 17 yr
        self.assertIs(peter.is_under_age(datetime_obj, 16), False) # 35 yr
