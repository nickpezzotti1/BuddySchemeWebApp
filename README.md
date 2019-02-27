# BuddySchemeWebApp (Python 3.6)
Buddy scheme management system web application. 

# Notes for developers
We are using pythons virtual enviorements to make sure we are all using the same version of the dependencies and of python. Python 3.6> is used.

## Setting up the v-enviorment

1. Check you have virtualenv on your machine, or download it.
2. `$ python3 -m venv env`
3. `$ source env/bin/activate`
4. `$ pip install -r requirements.txt`
5. `$ aws configure`
6. You will be asked to input AWS credentials (check chat description for latest).
7. Run the application



## Run the application

1. `$ source env/bin/activate`
2. `(env) $ python app.py`


## Setup Local SMTP Server

For debugging purposes, setup a local SMTP Server to send emails to while we don't use Amazon's SES

1. `(env) $ python3 -m smtpd -c DebuggingServer -n localhost:1025`
