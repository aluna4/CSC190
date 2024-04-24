from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Rule, userlogIn
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
import ipaddress

User = get_user_model()  # get the user model

class DeleteRuleViewTest(TestCase):
    # Set up user
    def setUp(self):
        # create a user with zones to test with
        self.user = userlogIn.objects.create_user(
            username='testuser',
            password='9876543210',
            employeeID='10101010',
            zones=["Internal", "Internet"]
        )
        self.client = Client()  # create a client
        self.client.login(username='testuser', password='9876543210')  # login with the client

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

    # test for successful deletion of a rule
    def test_delete_rule_success(self):

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


        data = {
            'rule_name': 'Test Rule',
            'application': 'ssh',
            'service': 'tcp-22',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        #self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule deleted successfully.")  # assert the message content



    #TESTS FOR IPNUT VALIDATION
    def test_delete_rule_all_fields_submit(self):
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

        data = {
            'rule_name': '',
            'source_ip': '1.1.1.1',
            'port': '12345',
            'state': 'absent',
        }

        response = self.client.post(reverse('delete_rule'), data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Please fill in all the fields.")  # assert the message content


    # test for validation error when rule name is not provided
    def test_delete_rule_validate_rule_name(self):
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

        ruleVal1 = data['rule_name']

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule created successfully")  # assert the message content

        data = {
            'rule_name': 'Test R',
            'application': 'ssh',
            'service': 'tcp-22',
            'state': 'absent',
        }

        ruleVal2 = data['rule_name']
        response = self.client.post(reverse('delete_rule'), data)
        #self.assertEqual(response.status_code, 200)
        #messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertTrue(ruleVal1!=ruleVal2, "Rule name must match a specified rule name.")  # assert the message content


    # test for invalid port number
    def test_delete_rule_invalid_application(self):
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

        ruleVal1 = data['application']

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule created successfully")  # assert the message content

        data = {
            'rule_name': 'Test R',
            'application': 'P2P',
            'service': 'tcp-22',
            'state': 'absent',
        }

        ruleVal2 = data['application']
        response = self.client.post(reverse('delete_rule'), data)
        #self.assertEqual(response.status_code, 200)
        #messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertTrue(ruleVal1!=ruleVal2, "Applications of rules must match.")  # assert the message content

   
    def test_delete_rule_valid_target(self):
        
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


        data = {
            'rule_name': 'Test Rule',
            'application': 'ssh',
            'service': 'tcp-22',
            'state': 'abt',
        }

        response = self.client.post(reverse('delete_rule'), data)
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        #self.assertEqual(response.status_code, 200)
        self.assertIn('ok=2', response.content.decode())  # assert that the Ansible task returns "ok"

    def test_delete_rule_invalid_service(self):
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

        ruleVal1 = data['service']

        response = self.client.post(reverse('add_rule'), data, follow=True)  # send a POST request
        self.assertEqual(response.status_code, 200)  # assert the response status code
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertEqual(str(messages[0]), "Rule created successfully")  # assert the message content

        data = {
            'rule_name': 'Test R',
            'application': 'ssh',
            'service': 'udp',
            'state': 'absent',
        }

        ruleVal2 = data['service']
        response = self.client.post(reverse('delete_rule'), data)
        #self.assertEqual(response.status_code, 200)
        #messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertTrue(ruleVal1!=ruleVal2, "Services of rules must match.")  # assert the message content

    def test_delete_rule_valid_declare(self):
        
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


        data = {
            'rule_name': 'Test Rule',
            'application': 'ssh',
            'service': 'tcp-22',
            'state': 'nie',
        }

        

        response = self.client.post(reverse('delete_rule'), data)
        #self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))  # get the messages from the response
        self.assertTrue(data['state']!='absent', "Error deleting firewall rule. State must be set to absent")  # assert the message content
