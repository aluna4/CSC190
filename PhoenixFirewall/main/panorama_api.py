import os
from panos import network
from panos import firewall
from dotenv import load_dotenv, find_dotenv
import subprocess
from pathlib import Path
import tempfile

# import user and pass from environment variables
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')
VAULT_PASS = os.getenv('VAULT_PASS')  # get the vault password from the environment

# check if VAULT_PASS is set, if not raise an exception
if not VAULT_PASS:
    raise ValueError("Vault password not found. Make sure VAULT_PASS is set in your .env file.")

# define the base directory from the PROJECT_ROOT environment variable
project_root = Path(os.getenv('PROJECT_ROOT', '.'))

# construct paths relative to the project root
ansible_dir = project_root / 'CSC190/PhoenixFirewall/ansible'

# when running the playbook, set the VAULT_PASS environment variable
def run_playbook(playbook_path, ansible_dir):
    # get the vault password from the environment variable
    vault_pass = os.getenv('VAULT_PASS')
    if vault_pass is None:
        raise ValueError("Vault password not set in environment variables")

    # create a temporary file to store the vault password
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write(vault_pass)
        vault_password_file = tmp.name
    
    try:
        # command to run ansible playbook with the vault password file
        command = [
            "ansible-playbook", "-i", "hosts", str(playbook_path),
            "--vault-password-file", vault_password_file
        ]
        subprocess.run(command, check=True, cwd=str(ansible_dir))
    finally:
        # ensure that the temporary file is removed after the playbook runs
        os.remove(vault_password_file)

# add firewall rule
def add_firewall_rule(rule_name, source_zone, source_ip, destination_zone, destination_ip, application, service, action):
  # ansible playbook template for adding a firewall rule
  playbook_template = """
---
- name: Create security policies
  hosts: phoenix_firewall
  connection: local
  vars_files:
    - nic_vault.txt

  vars:
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
  playbook_path = ansible_dir / 'create-security-policies.yml'
  with open(playbook_path, 'w') as file:
    file.write(playbook_content)
  
  # run ansible playbook
  run_playbook(playbook_path, ansible_dir)

  return True

def delete_firewall_rule(rule_name, source_ip, port):
  # Ansible playbook template for deleting a firewall rule
  playbook_template = """
---
- name: Delete security rule
  hosts: phoenix_firewall
  connection: local
  vars_files:
    - nic_vault.txt

  vars:
    device:
      ip_address: "{{{{ ip_address }}}}"
      username: "{{{{ username }}}}"
      password: "{{{{ password }}}}"
    
  collections:  
    - paloaltonetworks.panos

  tasks:
    - name: Delete rule
      paloaltonetworks.panos.panos_security_rule:
        provider: "{{{{ device }}}}"
        rule_name: "{rule_name}"
        source_ip: "{source_ip}"
        port: 12345
        state: 'absent'
"""
  # create ansible playbook
  playbook_content = playbook_template.format(
    rule_name=rule_name,
    source_ip=source_ip,
    port=port,
    ansible_python_interpreter=str((project_root / 'CSC190/venv/bin/python3'))
  )

  # create ansible playbook
  playbook_path = ansible_dir / 'delete-all-rules.yml'
  with open(playbook_path, 'w') as file:
    file.write(playbook_content)
  
  # run ansible playbook
  run_playbook(playbook_path, ansible_dir)

  return True

def commit_firewall_rule(rule_name, destination_zone, port):
  # ansible playbook template for committing a firewall rule
  playbook_template = """
---
- name: Commit firewall change
  hosts: phoenix_firewall
  connection: local
  vars_files:
    - nic_vault.txt

  vars:
    device:
      ip_address: "{{{{ ip_address }}}}"
      username: "{{{{ username }}}}"
      password: "{{{{ password }}}}"

  collections:
    - paloaltonetworks.panos

  tasks:
    - name: Commit candidate configuration
      paloaltonetworks.panos.panos_commit_firewall:
        provider: "{{{{ device }}}}"
      register: results

    - debug:
        msg: "Commit with Job ID: {{{{ results.jobid }}}} had output: {{{{ results.details }}}}"
"""
  # create ansible playbook
  playbook_content = playbook_template.format(
    rule_name=rule_name,
    destination_zone=destination_zone,
    port=port,
    ansible_python_interpreter=str((project_root / 'CSC190/venv/bin/python3'))
  )

  # create ansible playbook
  playbook_path = ansible_dir / 'commit-firewall-rule.yml'
  with open(playbook_path, 'w') as file:
    file.write(playbook_content)

  # run ansible playbook
  run_playbook(playbook_path, ansible_dir)

  return True
