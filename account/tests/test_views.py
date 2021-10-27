from django.test import TestCase
from django.test import Client

class SiteUserLoginTest(TestCase):
    def test_email_not_exist(self):
        c = Client()
        response = c.post('/signin', {'email': 'john@test.com', 'password': 'smith'})
        self.assertIs(response.status_code, 200)
        self.assertIs('<strong>Login Failed - Email does not exist.</strong>' in str(response.content), True)
