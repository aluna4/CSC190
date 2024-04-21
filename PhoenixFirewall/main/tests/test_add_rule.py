from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Rule, userlogIn
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
import ipaddress

User = get_user_model()  # get the user model

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
    
    def test_add_rule_success(self):
        # data for successful rule creation
        data = {
            'rule_name': 'Test Rule',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.1',
            'destination_zone': 'Internet',
            'destination_ip': '10.0.0.129',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request

        self.assertEqual(response.status_code, 200)  # assert the response status code

        self.assertTrue(Rule.objects.filter(rule_name='Test Rule').exists())  # assert that the rule exists
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule created successfully")  # assert the message content

    # tests for zone access or non-allowed flows
    def test_add_rule_disallowed_flow(self):
        # data for disallowed flow rule
        data = {
            'rule_name': 'Disallowed Rule',
            'source_zone': 'DMZ',
            'source_ip': '10.0.0.65',
            'destination_zone': 'Other',
            'destination_ip': '10.0.0.193',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request

        self.assertEqual(response.status_code, 200)  # assert the response status code
        self.assertFalse(Rule.objects.filter(rule_name='DISALLOWED RULE').exists())  # assert that the rule does not exist
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), 'The specified flow is not allowed.')  # assert the message content
    
    def test_add_rule_validation_error(self):
        # data for rule with validation error
        data = {
            'rule_name': 'Test Rule2',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.10',
            'destination_zone': 'Internet',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data)  # send a POST request

        self.assertEqual(response.status_code, 200)  # assert the response status code
        self.assertFormError(response, 'form', 'destination_ip', 'This field is required.')  # assert the form error

    def test_add_rule_invalid_data(self):
        # data for rule with invalid data
        data = {
            'rule_name': 'Test Rule',
            'source_zone': 'Internal',
            'source_ip': '192.168.1.1',
            'destination_zone': 'Internet',
            'destination_ip': 'invalid_ip',  
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data)  # send a POST request

        self.assertEqual(response.status_code, 200)  # assert the response status code
        self.assertFormError(response, 'form', 'destination_ip', 'Enter a valid IPv4 or IPv6 address.')  # assert the form error

    def test_add_rule_back_button(self):
        response = self.client.get(reverse('add_rule'))  # send a GET request

        self.assertContains(response, '<a href="{}">'.format(reverse('user')), html=True)  # assert the presence of a specific HTML element
