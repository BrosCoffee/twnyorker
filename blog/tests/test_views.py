from django.test import TestCase

class BlogTest(TestCase):
    def test_details(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/blog/', {'title': 'test', 'tag': ''})
        self.assertEqual(response.status_code, 200)
