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
	def setUp(self):
		# The default password
		self.password = '123'

		# Create superuser
		self.superuser = User.objects.create_superuser(username='Admin', password=self.password)
		self.superuser_password = self.password

		# Create regular users
		self.user1 = User.objects.create_user(username='User 1', password=self.password)
		self.user1_password = self.password
		self.user2 = User.objects.create_user(username='User 2', password=self.password)

		# The site's domain name, ex: example.com.
		self.domain = Site.objects.get(pk=settings.SITE_ID).domain
		# The site's protocol, ex: http or https
		self.protocol = 'https' if settings.USE_HTTPS else 'http'