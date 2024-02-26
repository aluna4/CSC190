import json

from units.compat import unittest
from units.compat.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from ansible.modules.namespace import my_module

def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS':args})
    basic._ANSIBLE_ARGS = to_bytes(args)

class AnsibleExitJson(Exception):
    pass

class AnsibleFailJson(Exception):
    pass

def exit_json(*args, kwargs**):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson

def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

def get_bin_path(self, arg, required=False):
    if arg.endswith('my_command'): #placeholder
        return '/home/malk/CSC190/PhoenixFirewall/ansible'
    else:
        if required:
            fail_json(msg='%r not found!' % arg)

class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json, get_bin_path=get_bin_path)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

def test_module_fail_when_required_args_missing(self):
    with self.assertRaises(AnsibleFailJson):
        set_module_args({})
        my_module.main()

test_ensure_command_called(self):
    set_module_args({'param1':10, 'param2':'test',})
    with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command: #command is changeable
        stdout = 'configuration updated'
        stderr = ''
        rc = 0
        mock_run_command.return_value = rc, stdout, stderr

        with self.assertRaises(AnsibleExitJson) as result:
            my_module.main()
        self.assertFalse(result.exception.args[0]['changed'])

    mock_run_command.assert_called_once_with('/home/malk/CSC190/PhoenixFirewall/ansible/XXCommandNameXX --value 10 --name test')
            
