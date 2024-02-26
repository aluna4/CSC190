import os
from panos import network
from panos import firewall
from dotenv import load_dotenv, find_dotenv
import subprocess
from pathlib import Path

# import user and pass from environment variables
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')

# define the base directory from the PROJECT_ROOT environment variable
project_root = Path(os.getenv('PROJECT_ROOT', '.'))

# construct paths relative to the project root
ansible_dir = project_root / 'CSC190/PhoenixFirewall/ansible'
playbook_path = ansible_dir / 'create-security-policies.yml'
vault_pass_file = ansible_dir / 'nic_vault_pass.txt'

# add firewall rule
def add_firewall_rule(rule_name, source_zone, source_ip, destination_zone, destination_ip, application, service, action):
    playbook_template = """
---
- name: Create security policies
  hosts: phoenix_firewall
  connection: local
  vars_files:
    - nic_vault.txt

  vars:
    ansible_python_interpreter: "{ansible_python_interpreter}"
    device:
      ip_address: "{{{{ ip_address }}}}"
      username: "{{{{ username }}}}"
      password: "{{{{ password }}}}"

  collections:
    - paloaltonetworks.panos

  tasks:
    - name: Add rule
      paloaltonetworks.panos.panos_security_rule:
        provider: "{{{{ device }}}}"
        rule_name: "{rule_name}"
        source_zone: ["{source_zone}"]
        source_ip: ["{source_ip}"]
        destination_zone: ["{destination_zone}"]
        destination_ip: ["{destination_ip}"]
        application: ["{application}"]
        service: ["{service}"]
        action: "{action}"
    """

    # create ansible playbook
    playbook_content = playbook_template.format(
        rule_name=rule_name,
        source_zone=source_zone,
        source_ip=source_ip,
        destination_zone=destination_zone,
        destination_ip=destination_ip,
        application=application,
        service=service,
        action=action,
        ansible_python_interpreter=str((project_root / 'CSC190/venv/bin/python3'))
    )
    with open(playbook_path, 'w') as file:
        file.write(playbook_content)
    
    # run ansible playbook
    command = ["ansible-playbook", "-i", "hosts", "--vault-password-file", str(vault_pass_file), str(playbook_path)]
    subprocess.run(command, check=True, cwd=str(ansible_dir))

    return True


