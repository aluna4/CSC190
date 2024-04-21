from django.test import TestCase
from django.urls import reverse
from PhoenixFirewall.main.models import DeleteRule

class DeleteRuleViewTest(TestCase):
    # test for successful deletion of a rule
    def test_delete_rule_success(self):
        data = {
            'rule_name': 'Test Rule',
            'source_ip': '1.1.1.1',
            'port': '12345',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue((DeleteRule.objects.filter(state=='absent')))

    # test for validation error when rule name is not provided
    def test_delete_rule_validation_error(self):
        data = {
            'source_ip': '1.1.1.1',
            'port': '12345',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'rule_name', 'Rule Name is required')

    # test for invalid port number
    def test_delete_rule_invalid_port(self):
        data = {
            'rule_name': 'Test Rule',
            'source_ip': '1.1.1.1',
            'port': '125',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'port', 'Port must be 12345.')

    # test for invalid rule name
    def test_delete_rule_invalid_name(self):
        data = {
            'source_ip': '1.1.1.1',
            'port': '12345',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'rule_name', 'Rule name must be specified.')

    # test for back button functionality
    def test_delete_rule_back_button(self):
        response = self.client.get(reverse('delete_rule'))
        self.assertContains(response, '<a href="{}">'.format(reverse('user')), html=True)
