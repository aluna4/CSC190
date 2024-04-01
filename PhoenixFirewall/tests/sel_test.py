import csv
import requests
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Global Variables
URL="http://127.0.0.1:8000/"

class Test(unittest.TestCase):
    # Setup method to initialize variables and objects
    def setUp(self):
        # Selenium options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # Starting the actual chrome service
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Stop the headless firefox browser for cleanup
    def tearDown(self):
        self.addClassCleanup(self.driver.quit)

    # Method to test status codes 
    def test_status_codes(self):
        # Object instantiations
        endpoint = Endpoint()

        # Unautheticated Endpoint Status Code Testing
        uauth_endpoints = endpoint.get_unauthenticated_endpoints()
        for ep in uauth_endpoints:
            endpoint_status_code = endpoint.get_status_code(ep)
            self.assertEqual(endpoint_status_code, 200, msg=f"{ep} does not have a 200 OK")

        # Authenticated Endpoint Status Code Testing
        # TODO: Implement authentication to webapp
        auth_endpoints = endpoint.get_autheticated_endpoints()

# Class to read csv files
class DocumentReader():
    # Read CSV file and parse it for endpoints. Return a list of endpoints
    def read(self, filename):
        endpoints = [URL]
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for endpoint in reader:
                endpoints.append(URL+str(endpoint[0]))
        return endpoints

# Class for endpoint objects
class Endpoint():
    # Object instantiations
    reader = DocumentReader()

    # Return unauthenticated endpoints
    def get_unauthenticated_endpoints(self):
        return self.reader.read("uEP.csv")
    
    # Return authenticated endpoints
    def get_autheticated_endpoints(self):
        return self.reader.read("aEP.csv")

    # Return status code of given endpoint
    def get_status_code(self, endpoint):
        r = requests.get(endpoint, verify=False)
        return r.status_code
        

# Run test cases
if __name__=='__main__':
    # Initializing Tests
    unittest.main(verbosity=2)