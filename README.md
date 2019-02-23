# BuddySchemeWebApp (Python 3.6)
Buddy scheme management system web application. 

# Notes for developers
We are using pythons virtual enviorements to make sure we are all using the same version of the dependencies and of python. Python 3.6> is used.

## Setting up the v-enviorment

1. Check you have virtualenv on your machine, or download it.
2. `$ python3 -m venv env`
3. `$ source env/bin/activate`
4. `$ pip install -r requirements.txt`
7. Set up the database*:  
  7.1 `(env) $ export BUDDY_DB_USER='admin'`  
  7.2 `(env) $ export BUDDY_DB_PASSWORD='r5!!eXFNVC5qMDL3$o&m'`  
8. Run the application

*To set the variables permanently, you should edit your `.bashrc` in your home directory.

## Run the application

1. `$ source env/bin/activate`
2. `(env) $ python app.py`

## Connect to database

(Assumption) mysql is installed on your machine

1. `(env) $ mysql -h buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com -u admin -p`
2. Enter the password: `r5!!eXFNVC5qMDL3$o&m`
3. `Use Buddy;`

## Setup Local SMTP Server

For debugging purposes, setup a local SMTP Server to send emails to while we don't use Amazon's SES

1. `(env) $ python3 -m smtpd -c DebuggingServer -n localhost:1025`
