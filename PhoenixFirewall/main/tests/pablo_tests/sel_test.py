import os
import csv
import requests
import unittest
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# global variables
URL="http://127.0.0.1:8000/"

class EndpointTest(unittest.TestCase):
    # setup method to initialize variables and objects
    def setUp(self):
        # selenium options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # starting the actual chrome service
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # stop the headless firefox browser for cleanup
    def tearDown(self):
        self.addClassCleanup(self.driver.quit)

    # method to test status codes 
    def test_status_codes(self):
        # object instantiations
        endpoint = Endpoint()

        # unautheticated endpoint status code testing
        uauth_endpoints = endpoint.get_unauthenticated_endpoints()
        for ep in uauth_endpoints:
            endpoint_status_code = endpoint.get_status_code(ep)
            self.assertEqual(endpoint_status_code, 200, msg=f"{ep} does not have a 200 OK")

class ExternalTest(unittest.TestCase):
    # setup method
    def setUp(self) -> None:
        # varibles for config
        load_dotenv(find_dotenv())
        self.USER=os.getenv('PHOENIX_USER')
        self.PASS=os.getenv('PHOENIX_PASS')
        self.PAN_URL=os.getenv('PAN_URL')
        self.r = requests.get(URL, verify=False)
    
    # teardown method
    def tearDown(self) -> None:
        # there is nothing to actually clean up during this test at the time
        pass
    
    # check firewall status
    def test_firewall_status(self) -> None:
        self.assertEqual(self.r.status_code, 200, msg=f"{self.PAN_URL} does not have a 200 OK. Firewall down.")
    
    # check firewall credentials
    def test_firewall_credentials(self) -> None:
        # send POST request to check credentials in firewall
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        data = {"user":f"{self.USER}", "password":f"{self.PASS}"}
        req = None
        try:
            req = requests.post(f"{self.PAN_URL}api/", data=data, headers=headers, verify=False)
        except:
            self.failIf(req = None, msg="Credential Check Failed")

# class to read csv files
class DocumentReader():
    # read CSV file and parse it for endpoints. Return a list of endpoints
    def read(self, filename) -> list:
        endpoints = [URL]
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for endpoint in reader:
                endpoints.append(URL+str(endpoint[0]))
        return endpoints

# class for endpoint objects
class Endpoint():
    # object instantiations
    reader = DocumentReader()

    # return unauthenticated endpoints
    def get_unauthenticated_endpoints(self) -> list:
        return self.reader.read("uEP.csv")
    
    # return authenticated endpoints
    def get_autheticated_endpoints(self) -> list:
        return self.reader.read("aEP.csv")

    # return status code of given endpoint
    def get_status_code(self, endpoint) -> int:
        r = requests.get(endpoint, verify=False)
        return r.status_code
        

# run test cases
if __name__=='__main__':
    # initializing tests
    unittest.main(verbosity=2)
