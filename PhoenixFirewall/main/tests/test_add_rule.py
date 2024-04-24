from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Rule, userlogIn
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
import ipaddress

User = get_user_model()  # get the user model

############### SETUP ###############
class AddRuleViewTest(TestCase):
    def setUp(self):
        # create a user with zones to test with
        self.user = userlogIn.objects.create_user(
            username='testuser',
            password='12345678',
            employeeID='00000001',
            zones=["Internal", "Internet"]
        )
        self.client = Client()  # create a client
        self.client.login(username='testuser', password='12345678')  # login with the client

        self.ALLOWED_FLOWS = [
            ('Internal', 'DMZ'),
            ('Internal', 'Internet'),
            ('Internet', 'DMZ')
        ]
        self.ZONE_SUBNETS = {
            'Internal': ipaddress.ip_network('10.0.0.0/26'),
            'DMZ': ipaddress.ip_network('10.0.0.64/26'),
            'Internet': ipaddress.ip_network('10.0.0.128/26'),
            'Other': ipaddress.ip_network('10.0.0.192/26'),
        }
    

############### TEST RULE SUCCESS ###############
    def test_add_rule_success(self):
        # data for successful rule creation
        data = {
            'rule_name': 'Test Rule',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule created successfully")  # assert the message content



############### TEST BAD INPUT ###############
    def test_bad_rule_name(self):
        data = {
            'rule_name': '',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'Please fill in all the fields.')  # assert the message content

    def test_bad_source_zone(self):
        data = {
            'rule_name': 'bad_source_zone',
            'source_zone': 'bad_zone',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The specified source or destination zone is not allowed, or does not exist.')  # assert the message content

    def test_bad_destination_zone(self):
        data = {
            'rule_name': 'bad_destination_zone',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'bad_zone',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The specified source or destination zone is not allowed, or does not exist.')  # assert the message content

    def test_bad_source_ip(self):
        data = {
            'rule_name': 'rulename',
            'source_zone': 'Internal',
            'source_ip': 'bad_format',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "The IP address entered is not in the correct format (x.x.x.x).")  # assert the message content

    def test_bad_dest_ip(self):
        data = {
            'rule_name': 'rulename',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': 'bad_format',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "The IP address entered is not in the correct format (x.x.x.x).")  # assert the message content

    def test_bad_application(self):
        data = {
            'rule_name': 'rulename',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'bad_application',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertIn("returned non-zero exit status 2.", str(messages[0]))  # assert that the message content contains the specified string

    def test_bad_service(self):
        data = {
            'rule_name': 'rulename',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'bad_service',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertIn("returned non-zero exit status 2.", str(messages[0]))  # assert that the message content contains the specified string

############### TEST WRONG INPUT ###############
    def test_ip_in_wrong_zone(self):
        data = {
            'rule_name': 'rulename',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.130',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }
        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The IP address entered is not within the correct zone.')  # assert the message content

    def test_add_rule_no_zone_access(self):
        data = {
            'rule_name': 'no_zone_access',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'DMZ',
            'destination_ip': '10.0.0.65',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The specified flow is not allowed. You do not have access to a zone')  # assert the message content

    def test_bad_flow(self):
        data = {
            'rule_name': 'no_zone_access',
            'source_zone': 'Internet',
            'source_ip': '10.0.0.129',
            'destination_zone': 'Internal',
            'destination_ip': '10.0.0.1',
            'application': 'ssh',
            'service': 'tcp-22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request

        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The specified flow is not allowed.')  # assert the message content

