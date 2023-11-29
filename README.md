![](https://lh7-us.googleusercontent.com/Q5qISaC80enw9vhh_JmkwlelJS5Kkxu_U5Oy03W-LZ7wMiQUXAb2MhCGINlo3p8Ft8Lvy-j1uT8bh09CySWQZFcyg8GRVQoeQ3VskPOTfi_cfD356djTSzpTgreCIgoiUV_o2vDvsYpfx6o=s2048)

## Installation Guide
1) Clone this repository
	1) `git clone https://github.com/aluna4/CSC190.git`
2) Navigate into the `CSC190` directory
	1) `cd CSC190`
3) Install python virtual environments
	4) `sudo apt install python3-venv`
4) Create a virtual environment within the root folder
	1) `python3 -m venv venv`
5) Navigate into the virtual environment 
	1) `source venv/bin/activate`
6) Download and install the dependencies
	2) `pip3 install -r requirements.txt`
7) Navigate to the main runner for the application
	1) `cd PhoenixFirewall`
8) Run the PhoenixFirewall application
	1) `python3 manage.py runserver`

## PhoenixFirewall
PhoenixFirewall is meant to streamline the process of firewall amendment requests as well as help set up complete firewalls from configs. Rather than having continuous pipelines with developers creating tickets to amend the firewall and having administrators go in and manually accept/decline each request, PhoenixFirewall is aiming to make it so that developers can create rules directly on the firewall using specifically crafted requests with a definite scope. One of the main purposes of PhoenixFirewall  is to deploy and modify Palo Alto specific firewalls.  Utilizing Palo Alto's native API as well as Django's native API, PhoenixFirewall will create routes and workflows to alter the Palo Alto firewall as defined by an administrative user.

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