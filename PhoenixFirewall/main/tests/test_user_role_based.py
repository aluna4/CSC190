from django.test import Client
from PhoenixFirewall.main.tests import BaseTestCase

class UserRoleBasedContentTest(BaseTestCase):
    def setUp(self):
        # create test users
        super().setUp()
        self.client = Client()

    def test_superuser_content(self):
        # log in as superuser
        self.client.login(username='adnmin', password='password')
        
        # make a request to the page that renders the template
        response = self.client.get('admin')
        
        # assert that the response contains content specific to the superuser role
        self.assertContains(response, 'Role: Superuser')
        self.assertContains(response, 'Username: superuser')

    def test_regular_user_content(self):
        # log in as regular user
        self.client.login(username='regularuser', password='password')
        
        # make a request to the page that renders the template
        response = self.client.get('user')
        
        # assert that the response contains content specific to the regular user role
        self.assertContains(response, 'Role: User')
        self.assertContains(response, 'Username: regularuser')
