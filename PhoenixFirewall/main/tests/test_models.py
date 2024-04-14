from django.test import TestCase
from main.models import userlogIn, Rule
from django.utils import timezone

class UserModelTest(TestCase):
    #tests the creation of a user
    def test_user_creation(self):
        user = userlogIn.objects.create(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            user_pswd="password",
            employeeID="123456",
            create_date=timezone.now(),
            zones=[]
        )
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.user_name, "johndoe")
        self.assertEqual(user.user_pswd, "password")
        self.assertEqual(user.employeeID, "123456")
        self.assertIsNotNone(user.create_date)
    
    def test_user_str_representation(self):
        user = userlogIn.objects.create(
            first_name="Jane",
            last_name="Smith",
            user_name="janesmith",
            user_pswd="password",
            employeeID="789012",
            create_date=timezone.now(),
            zones=[]
        )
        self.assertEqual(str(user), "Employee: 789012, Username = janesmith")

    def test_user_unique_constraint(self):
        user1 = userlogIn.objects.create(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            user_pswd="password",
            employeeID="123456",
            create_date=timezone.now(),
            zones=[]
        )
        with self.assertRaises(Exception):
            user2 = userlogIn.objects.create(
                first_name="Jane",
                last_name="Smith",
                user_name="johndoe",  # Trying to use same username
                user_pswd="password",
                employeeID="789012",
                create_date=timezone.now(),
                zones=[]
            )

class RuleModelTest(TestCase):
    def test_rule_creation(self):
        rule = Rule.objects.create(
            employeeID=self.user,
            rule_name="test_rule",
            source_zone="zone1",
            source_ip="192.168.1.1",
            destination_zone="zone2",
            destination_ip="192.168.2.2",
            application="app",
            service="service",
            action="allow"
        )
        self.assertTrue(isinstance(rule, Rule))
        self.assertEqual(rule.rule_name, "test_rule")
        self.assertEqual(rule.source_zone, "zone1")
        self.assertEqual(rule.source_ip, "192.168.1.1")
        self.assertEqual(rule.destination_zone, "zone2")
        self.assertEqual(rule.destination_ip, "192.168.2.2")
        self.assertEqual(rule.application, "app")
        self.assertEqual(rule.service, "service")
        self.assertEqual(rule.action, "allow")

    def test_rule_str_representation(self):
        rule = Rule.objects.create(
            employeeID=self.user,
            rule_name="test_rule",
            source_zone="zone1",
            source_ip="192.168.1.1",
            destination_zone="zone2",
            destination_ip="192.168.2.2",
            application="app",
            service="service",
            action="allow"
        )
        self.assertEqual(str(rule), f"Employee: {self.user.employeeID}Rule Name = {rule.rule_name}")
