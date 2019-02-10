# BuddySchemeWebApp
Buddy scheme management system web application. 

# Setting up on your local dev machine

## One-time setup

1. Check you have virtualenv on your machine, or download it.
2. `$ virtualenv env`
3. `$ source env/bin/activate`
4. `$ pip install -r requirements.txt`

`$ deactivate` to exit

## Running the app

1. `$ source env/bin/activate`
2. `(env) $ python app.py`

## Datababse credentials
To set the variables permanently, you should edit your `.bashrc` in your home directory.

1. `(env) $ export BUDDY_DB_USER='admin'`
2. `(env) $ export BUDDY_DB_PASSWORD='r5!!eXFNVC5qMDL3$o&m'`

## Connect to databse

1. `(env) $ mysql -h buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com -u admin -p`
