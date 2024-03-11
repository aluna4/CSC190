from ansibleUnitScripts import *
from unittest.mock import MagicMock, PropertyMock, patch
from panos.errors import PanDeviceError
from panos.firewall import Firewall
from panos.panorama import DeviceGroup, Panorama, Template, TemplateStack
from panos.policies import PostRulebase, PreRulebase, Rulebase

firewall_mock()
panorama_mock()

