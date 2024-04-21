from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from django.test import TestCase
import environ


env = environ.Env(
	# set casting, default value
	DEBUG=(bool, False)
)

User = get_user_model()


class BaseTestCase(TestCase):
	"""
	This class serves as the base test case for all test cases in the 'main.tests' module.
	It provides setup and utility methods that can be used by the derived test cases.
	"""

	def setUp(self):
		# the default password
		self.password = '123'

		# create superuser
		self.superuser = User.objects.create_superuser(username='Admin', password=self.password)
		self.superuser_password = self.password

		# create regular users
		self.user1 = User.objects.create_user(username='User 1', password=self.password)
		self.user1_password = self.password
		self.user2 = User.objects.create_user(username='User 2', password=self.password)

		# the site's domain name, ex: example.com.
		self.domain = Site.objects.get(pk=settings.SITE_ID).domain
		# the site's protocol, ex: http or https
		self.protocol = 'https' if settings.USE_HTTPS else 'http'