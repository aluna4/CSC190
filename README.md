![](https://lh7-us.googleusercontent.com/Q5qISaC80enw9vhh_JmkwlelJS5Kkxu_U5Oy03W-LZ7wMiQUXAb2MhCGINlo3p8Ft8Lvy-j1uT8bh09CySWQZFcyg8GRVQoeQ3VskPOTfi_cfD356djTSzpTgreCIgoiUV_o2vDvsYpfx6o=s2048)

## PhoenixFirewall
PhoenixFirewall is meant to streamline the process of firewall amendment requests as well as help set up complete firewalls from configs. Rather than having continuous pipelines with developers creating tickets to amend the firewall and having administrators go in and manually accept/decline each request, PhoenixFirewall is aiming to make it so that developers can create rules directly on the firewall using specifically crafted requests with a definite scope. One of the main purposes of PhoenixFirewall  is to deploy and modify Palo Alto specific firewalls.  Utilizing Palo Alto's native API as well as Django's native API, PhoenixFirewall will create routes and workflows to alter the Palo Alto firewall as defined by an administrative user.

## Installation Guide
1) Clone this repository
	1) `git clone https://github.com/aluna4/CSC190.git`
2) Navigate into the `CSC190` directory
	1) `cd CSC190`
3) Create a `.env` file
	1) `touch .env`
2) Populate the `.env` file with variables as follows:
	1) NOTE: Change `SECRET_KEY` when running in production. 
   ```
   PHOENIX_USER="Palo Alto Firewall Username"
   PHOENIX_PASS="Palo Alto Firewall User Password"
   SECRET_KEY="django-insecure-u2&7**ao7+($5*y$_o*xpy(al94(ls@)hd5_k#%m#nkul+7@(%"
   PAN_URL="YOUR PALO ALTO FIREWALL URL HERE"
   ```
1) Install python virtual environments
	1) `sudo apt install python3-venv`
2) Create a virtual environment within the root folder
	1) `python3 -m venv venv`
3) Navigate into the virtual environment 
	1) `source venv/bin/activate`
4) Download and install the dependencies
	1) `pip3 install -r requirements.txt`
5) Navigate to the main runner for the application
	1) `cd PhoenixFirewall`
6) Run the PhoenixFirewall application
	1) `python3 manage.py runserver`

## Visualization Demo
[Video Link](https://www.youtube.com/shorts/pWTXqm0EDjQ)

## Future Milestones
### Ansible Playbooks
A key element to our project is having the ability to spin up new Palo Alto firewalls using config files automatically. We are aiming to accomplish this by utilizing Ansible to store and mass-deploy firewall configurations

### Working Rule sets
Currently, we are working towards getting a running GUI and having inputs get parsed correctly. Once we figure out all the fields to get rules added to the firewall via the API, we can start getting real rule sets added.

## Q&A
### Q)  What stack is this project running?
A) We are running Django as our main tech stack. Our main languages include Python, CSS, and HTML as well as an SQLitev3 database that is native to Django.

### Q) How do I add users and groups?
A) You can navigate to the native Django admin panel and log in as a superuser. Once logged in, there are options on the left to add users and groups to use for the application authentication. 

## Testing
### Placeholder

## Deployment
### Placeholder

## Developer Instructions
### Placeholder
