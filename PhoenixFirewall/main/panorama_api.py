import os
from panos import network
from panos import firewall
from dotenv import load_dotenv, find_dotenv

# Import user and pass from environment variables.
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')

# add firewall rule
def add_firewall_rule(rule_name, ip, port):
    
    print(f"Adding firewall rule with Rule Name: {rule_name}, IP: {ip}, Port: {port}")

    ### actual panOS code

    return True
