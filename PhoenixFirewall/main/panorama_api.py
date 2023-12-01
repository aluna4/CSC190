import os
from panos import network
from panos import firewall
from dotenv import load_dotenv, find_dotenv
import subprocess

# Import user and pass from environment variables.
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')

# add firewall rule
def add_firewall_rule(rule_name, ip, port):
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
        source_zone: ["any"]
        source_ip: ["{source_ip}"]
        destination_zone: ["any"]
        destination_ip: ["destination-server"]
        application: ["ssh"]
        service: ["tcp-{service_port}"]
        action: "allow"
    """

    # create ansible playbook
    playbook_content = playbook_template.format(rule_name=rule_name, source_ip=ip, service_port=port)
    with open('/home/ubuntu/nic_190/CSC190/PhoenixFirewall/ansible/create-security-policies.yml', 'w') as file:
        file.write(playbook_content)
    
    # run ansible playbook
    command = ["ansible-playbook", "-i", "hosts", "--vault-password-file", "nic_vault_pass.txt","create-security-policies.yml"]
    subprocess.run(command, check=True, cwd="/home/ubuntu/nic_190/CSC190/PhoenixFirewall/ansible/")

    return True


