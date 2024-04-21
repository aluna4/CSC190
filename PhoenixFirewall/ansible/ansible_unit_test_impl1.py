import json
from units.compat import unittest
from units.compat.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from ansible.modules.namespace import my_module
import os

# set the module arguments
def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS':args})
    basic._ANSIBLE_ARGS = to_bytes(args)

class AnsibleExitJson(Exception):
    pass

class AnsibleFailJson(Exception):
    pass

# raise AnsibleExitJson exception with optional arguments
def exit_json(*args, kwargs**):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson

# raise AnsibleFailJson exception with optional arguments
def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

# get the binary path for a given argument
def get_bin_path(self, arg, required=False):
    if arg.endswith('my_command'): #placeholder
        project_root = os.getenv('PROJECT_ROOT')
        return f'{project_root}/CSC190/PhoenixFirewall/ansible'
    else:
        if required:
            fail_json(msg='%r not found!' % arg)

class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json, get_bin_path=get_bin_path)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

# test case for module failure when required arguments are missing
def test_module_fail_when_required_args_missing(self):
    with self.assertRaises(AnsibleFailJson):
        set_module_args({})
        my_module.main()

# test case to ensure command is called
def test_ensure_command_called(self):
    set_module_args({'param1':10, 'param2':'test',})
    with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command: #command is changeable
        stdout = 'configuration updated'
        stderr = ''
        rc = 0
        mock_run_command.return_value = rc, stdout, stderr

        with self.assertRaises(AnsibleExitJson) as result:
            my_module.main()
        self.assertFalse(result.exception.args[0]['changed'])

    project_root = os.getenv('PROJECT_ROOT')
    command = f'{project_root}/CSC190/PhoenixFirewall/ansible/XXCommandNameXX --value 10 --name test'
    mock_run_command.assert_called_once_with(command)
