from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import login_view, add_rule, delete_rule, commit_rule, user_view, admin_view, get_pan_security_config, upload, create_user_view

class TestUrls(SimpleTestCase):

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_add_rule(self):
        url = reverse('add_rule')
        self.assertEquals(resolve(url).func, add_rule)

    def test_delete_rule(self):
        url = reverse('delete_rule')
        self.assertEquals(resolve(url).func, delete_rule)

    def test_commit_rule(self):
        url = reverse('commit_rule')
        self.assertEquals(resolve(url).func, commit_rule)

    def test_user(self):
        url = reverse('user')
        self.assertEquals(resolve(url).func, user_view)

    def test_admin(self):
        url = reverse('admin')
        self.assertEquals(resolve(url).func, admin_view)

    def test_get_pan_security_config(self):
        url = reverse('get_pan_security_config')
        self.assertEquals(resolve(url).func, get_pan_security_config)

    def test_upload(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func, upload)

    def test_create_user(self):
        url = reverse('create_user')
        self.assertEquals(resolve(url).func, create_user_view)
