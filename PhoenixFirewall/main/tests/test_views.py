from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch
import ipaddress

# allowed flows based on simulated subnet segments
allowed_flows = [
    ('Internal', 'DMZ'),  # internal zone can communicate with DMZ zone
    ('Internal', 'Internet'),  # internal zone can communicate with internet zone
    ('Internet', 'DMZ')  # internet zone can communicate with DMZ zone
]

# zone to subnet mappings
zone_subnets = {
    'Internal': ipaddress.ip_network('10.0.0.0/26'),  # internal zone subnet
    'DMZ': ipaddress.ip_network('10.0.0.64/26'),  # DMZ zone subnet
    'Internet': ipaddress.ip_network('10.0.0.128/26'),  # internet zone subnet
    'Other': ipaddress.ip_network('10.0.0.192/26'),  # other zone subnet
}

class AddRuleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_rule_url = reverse('add_rule')
        self.allowed_flows = allowed_flows
        self.zone_subnets = zone_subnets

    def test_get_add_rule(self):
        # test GET request to add_rule view
        response = self.client.get(self.add_rule_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_rule.html')

    @patch('main.views.add_rule')  # patch add_firewall_rule method
    def test_post_add_rule_invalid_data(self, mock_add_rule):
        # test POST request to add_rule view with invalid data
        mock_add_rule.return_value = False  # assume rule addition will fail
        response = self.client.post(self.add_rule_url, {
            'rule_name': 'Test Rule',
            'source_zone': 'Internet',
            'destination_zone': 'Internal',
            'source_ip': '10.0.0.129',
            'destination_ip': '10.0.0.1',
            'application': 'http',
            'service': '80',
            'action': 'allow',
        })
        # get messages from the response
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'The specified flow is not allowed.' for message in messages_list))

    @patch('main.views.add_rule')  # patch add_firewall_rule method
    def test_post_add_rule_valid_data(self, mock_add_rule):
        # test POST request to add_rule view with valid data
        mock_add_rule.return_value = True  # assume rule addition will succeed
        response = self.client.post(self.add_rule_url, {
            'rule_name': 'Test Rule',
            'source_zone': 'DMZ',
            'destination_zone': 'Internal',
            'source_ip': '10.0.0.65',
            'destination_ip': '10.0.0.1',
            'application': 'http',
            'service': '12345',
            'action': 'allow',
        })
        # get messages from the response
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == "Rule created successfully" for message in messages_list))

        # since the view redirects after creating a rule, you also want to check that:
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, reverse('user'))  # check that it's the expected redirect URL
