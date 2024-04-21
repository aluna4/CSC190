from unittest.mock import MagicMock, PropertyMock, patch
from panos.errors import PanDeviceError
from panos.firewall import Firewall
from panos.panorama import DeviceGroup, Panorama, Template, TemplateStack
from panos.policies import PostRulebase, PreRulebase, Rulebase

__metaclass__ = type


# import pytest
# from ansible.module_utils.basic import AnsibleModule
# from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
#     get_connection,
# )


# run all tests with mocked firewall unless specified.
def firewall_mock(mocker):
    # create a mock Firewall object
    fw = Firewall("192.168.1.1", "admin", "password", "API_KEY")
    fw._version_info = (10, 0, 0)

    # patch the create_from_device method to return the mock Firewall object
    create_from_device_mock = mocker.patch(
        "panos.base.PanDevice.create_from_device", return_value=fw
    )
    return create_from_device_mock.return_value


# create a mock Panorama object
def panorama_mock(mocker):
    pano = Panorama("192.168.2.1", "admin", "password", "API_KEY")
    pano._version_info = (10, 0, 0)

    # patch the create_from_device method to return the mock Panorama object
    create_from_device_mock = mocker.patch(
        "panos.base.PanDevice.create_from_device", return_value=pano
    )

    the_dg = DeviceGroup(name="the_dg")
    the_template = Template(name="the_template")
    the_stack = TemplateStack(name="the_stack")

    # mock the refreshall methods to return the mock objects
    mocker.patch("panos.panorama.DeviceGroup.refreshall", return_value=[the_dg])
    mocker.patch("panos.panorama.Template.refreshall", return_value=[the_template])
    mocker.patch("panos.panorama.TemplateStack.refreshall", return_value=[the_stack])

    return create_from_device_mock.return_value


# more tests to be written
