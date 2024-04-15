from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Rule,userlogIn
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
import ipaddress

User = get_user_model()

class AddRuleViewTest(TestCase):
    def setUp(self):
        # Create a user with zones to test with
        self.user = userlogIn.objects.create_user(
            username='testuser',
            password='12345678',
            employeeID='00000001',
            zones=["Internal", "Internet"]
        )
        self.client = Client()
        self.client.login(username='testuser', password='12345678')

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

        response = self.client.post(reverse('add_rule'), data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Rule.objects.filter(rule_name='Test Rule').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Rule created successfully")

    #tests for zone access or non allowed flows
    def test_add_rule_disallowed_flow(self):
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

        response = self.client.post(reverse('add_rule'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Rule.objects.filter(rule_name='DISALLOWED RULE').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'The specified flow is not allowed.')
    
    def test_add_rule_validation_error(self):
        data = {
            'rule_name': 'Test Rule2',
            'source_zone': 'Internal',
            'source_ip': '10.0.0.10',
            'destination_zone': 'Internet',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'destination_ip', 'This field is required.')

    def test_add_rule_invalid_data(self):
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

        response = self.client.post(reverse('add_rule'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'destination_ip', 'Enter a valid IPv4 or IPv6 address.')

    def test_add_rule_back_button(self):
        response = self.client.get(reverse('add_rule'))

        self.assertContains(response, '<a href="{}">'.format(reverse('user')), html=True)
