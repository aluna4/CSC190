from django.test import Client
from PhoenixFirewall.main.tests.base import BaseTestCase

class UserRoleBasedContentTest(BaseTestCase):
    def setUp(self):
        # Create test users
        super().setUp()
        self.client = Client()

    def test_superuser_content(self):
        # Log in as superuser
        self.client.login(username='adnmin', password='password')
        
        # Make a request to the page that renders the template
        response = self.client.get('admin')
        
        # Assert that the response contains content specific to the superuser role
        self.assertContains(response, 'Role: Superuser')
        self.assertContains(response, 'Username: superuser')

    def test_regular_user_content(self):
        # Log in as regular user
        self.client.login(username='regularuser', password='password')
        
        # Make a request to the page that renders the template
        response = self.client.get('user')
        
        # Assert that the response contains content specific to the regular user role
        self.assertContains(response, 'Role: User')
        self.assertContains(response, 'Username: regularuser')
