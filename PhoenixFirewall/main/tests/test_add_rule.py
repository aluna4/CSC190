from django.test import TestCase
from django.urls import reverse
from PhoenixFirewall.main.models import FirewallRule

class AddRuleViewTest(TestCase):
    def test_add_rule_success(self):
        data = {
            'rule_name': 'Test Rule',
            'source_zone': 'Internal',
            'source_ip': '192.168.1.1',
            'destination_zone': 'Internet',
            'destination_ip': '8.8.8.8',
            'application': 'SSH',
            'service': '22',
            'action': 'allow',
        }

        response = self.client.post(reverse('add_rule'), data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(FirewallRule.objects.filter(rule_name='Test Rule').exists())

    def test_add_rule_validation_error(self):
        data = {
            'rule_name': 'Test Rule',
            'source_zone': 'Internal',
            'source_ip': '192.168.1.1',
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
