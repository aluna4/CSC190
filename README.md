![](https://lh7-us.googleusercontent.com/Q5qISaC80enw9vhh_JmkwlelJS5Kkxu_U5Oy03W-LZ7wMiQUXAb2MhCGINlo3p8Ft8Lvy-j1uT8bh09CySWQZFcyg8GRVQoeQ3VskPOTfi_cfD356djTSzpTgreCIgoiUV_o2vDvsYpfx6o=s2048)

## PhoenixFirewall
PhoenixFirewall is meant to streamline the process of firewall amendment requests as well as help set up complete firewalls from configs. Rather than having continuous pipelines with developers creating tickets to amend the firewall and having administrators go in and manually accept/decline each request, PhoenixFirewall is aiming to make it so that developers can create rules directly `python3 manage.py runserver` the firewall using specifically crafted requests with a definite scope. One of the main purposes of PhoenixFirewall  is to deploy and modify Palo Alto specific firewalls.  Utilizing Palo Alto's native API as well as Django's native API, PhoenixFirewall will create routes and workflows to alter the Palo Alto firewall as defined by an administrative user.

## Installation Guide 
Clone this repository
```
git clone https://github.com/aluna4/CSC190.git
```

Navigate into the `CSC190` directory
```
cd CSC190
```

Create a `.env` file
```
touch .env
```

Populate the `.env` file with variables as follows:
1) NOTE: Change `SECRET_KEY` when running in production. 
2) The project root is your path before the CSC190 folder on your system
   ```
   PHOENIX_USER="Palo Alto Firewall Username"
   PHOENIX_PASS="Palo Alto Firewall User Password"
   SECRET_KEY="YOUR SECRET KEY HERE"
   PAN_URL="YOUR PALO ALTO FIREWALL URL HERE"
   PROJECT_ROOT="/home/user/"
   VAULT_PASS="VAULT PASS HERE"
   VAULT_PASS="YOUR VAULT PASS HERE FOR ANSIBLE"
   ```

Install python virtual environments
```
sudo apt install python3-venv
```

Create a virtual environment within the root folder
```
python3 -m venv venv
```

Navigate into the virtual environment 

```
source venv/bin/activate
```

Download and install the dependencies
```
pip3 install -r requirements.txt
```

Navigate to the main runner for the application
```
cd PhoenixFirewall
```
 
Run the PhoenixFirewall application
```
python3 manage.py runserver
```

## Visualization Demo
[Video Link](https://www.youtube.com/shorts/pWTXqm0EDjQ)

## Q&A
### Q)  What stack is this project running?
A) We are running Django as our main tech stack. Our main languages include Python, CSS, and HTML as well as an SQLitev3 database that is native to Django.

### Q) How do I add users and groups?
A) You can navigate to the native Django admin panel and log in as a superuser. Once logged in, there are options on the left to add users and groups to use for the application authentication. 

### Q) What if I would like to change multiple firewalls at once?
A) You can opt to change your firewall address in the `.env` file or you can utilize Ansible to add multiple firewalls as options. 
## Testing
### Selenium Testing
To utilize Selenium based testing, run the script `sel_test.py`. This script can be found in the path `$PROJECT_ROOT/CSC190/PhoenixFirewall/tests`. The Selenium testing will check for API endpoint connections, firewall communication, and valid firewall credential. Check the `Developer Instructions` for more details on adding test cases. 

### Ansible Testing
To utilize Ansible based testing, run the command `python3 manage.py test`. This command should be ran from `$PROJECT_ROOT/CSC190/PhoenixFirewall`. This will run both the add rule tests and the delete rule tests.
To run a specific ansible test, run the command `python3 manage.py test main.test.[ansible_test_file]`.
There are scripts to run tests when adding rules, deleting rules, and committing the firewall. The tests run from the unittests python library and check valid rule names, existence of rules, proper credentials, and other inputs that could potentially be unsuccessful when running the specified ansible script.
To add more test cases:
   -First create a way to capture the invalid success in the `main.views` file. 
   -Then modify the respecitve ansible script to catch the invalid success in its own defined method.
Upon running the modified test file again, the new tests will be included in the tests result output. 


## Deployment
### AWS/Azure
To deploy in AWS or Azure, spin up a reasonable instance, AWS's T3 Micro or Azure's A-series instances, and create an instance.

Once in the instance, update and upgrade your instance to the most recent updates and follow the `Installation Guide` to deploy onto this instance.
### Self-Hosted
The self hosted instructions for deployment is under the `Installation Guide` above. This should pertain to any self hosted `Debian` or `Ubuntu` instance.

## Developer Instructions
### Testing
When utilizing the selenium based testing, you can put your endpoints within the `uEP.csv` file under the path `$PROJECT_ROOT/CSC190/PhoenixFirewall/tests`. The endpoint format should be `$ENDPOINT_NAME/` with the first line being `endpoints`.

The selenium and ansible testing is based on python's `unittest` library. To add more test cases, it is recommended to read on their documentation to add onto the existing code-base. 

### .ENV File
The `PAN_URL` variable takes both an ip address as well as a FQDN. 

Ensure your `SECRET_KEY` fits the Django standards for the key length as well as the usable characters within that key.

Ensure the `PROJECT_ROOT` variable is your absolute path right before the cloned repository, including the trailing `/`. 

### Deployment
Currently, the project has been created only to run in Django's developer mode. This is intentional, as the product was meant specifically to be used as an internal application. This gives the application administrators an easier time with logging and bug reduction. Some infrastructure changes may be required if future developers would like Django to run in production mode. 
