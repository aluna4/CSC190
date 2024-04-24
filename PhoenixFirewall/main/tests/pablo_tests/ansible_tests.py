#import mock
import pytest 
from ..main.panorama_api import add_firewall_rule
from pytest_mock import mocker
from src.jobitems import manager


def add_function_ansible(rule_name, src, src_ip, dest, dest_ip, app, service, action):
    return add_firewall_rule(rule_name, src, src_ip, dest, dest_ip, app, service, action)

def test_add():
    assert add_function_ansible('rule2', 'Internal', '1.1.1.1', 'Internet', '1.1.1.1', 'any', 'any', 'tcp')

#def inc(z):
 #   return z + 1

#def test():
  #  assert inc(3) == 4

def test_add_mock(mocker):
    mocker.patch.object(manager, 'sub-method')
    manager.sub_method.return_value = 120
    manager.method_under_test()

    manager.sub_method.assert_called_with('name1', 'src', '1.1.1.1',  'dest', '2.2.2.2', 'Internet', 'any', 'tcp')
