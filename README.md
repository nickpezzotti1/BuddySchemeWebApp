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
6. You will be asked to input AWS credentials (access credentials have been specified in the report).
7. Run the application


## Test the application

1. `$ source env/bin/activate`
2. `(env) $ pytest`

## Run the application

1. `$ source env/bin/activate`
2. `$ export FLASK_APP=flaskr`
3. `(env) $ flask run`

## Setup Local SMTP Server

As currently Amazon's SES (Simple Email Service) gets sent to KCL's junk email, we setup a local SMTP Server to send emails to. 
This allows you to read the emails being sent in terminal. 

To view the emails, run: 
1. `(env) $ python3 -m smtpd -c DebuggingServer -n localhost:1025`

