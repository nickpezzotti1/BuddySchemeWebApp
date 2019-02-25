import smtplib
from email.mime.text import MIMEText
import user
from auth_token import generate_token

COMMASPACE = ', '

def send_email(sender, recipients, subject, content):
    try:
        ## Run a local instance of a email server that echoes
        ## the messages on terminal
        ## (env) $ python3 -m smtpd -c DebuggingServer -n localhost:1025
        server = smtplib.SMTP("localhost", 1025)

        msg = MIMEText(content)
        msg['From'] = sender
        msg['To'] = COMMASPACE.join(recipients)
        msg["Subject"] = subject

        server.send_message(msg)
        server.close()
    except Exception as e:
        print(e)

def send_email_confirmation_to_user(user, secret_key):
    ## TODO: Possible feature to check if email
    #  was already confirmed and keep track of multiple requests
    token = generate_token(secret_key, user.k_number)
    sender = "no-reply@sbs.kcl.ac.uk"
    recipients = [str(user.k_number) + "@kcl.ac.uk"]
    subject = "Email Confirmation - Student Buddy System"
    path = "http://localhost:5000/confirm/"
    content = f"Welcome to KCL\'s Student Buddy System. \n Please activate your email at {path}{token}"

    send_email(sender, recipients, subject, content)


def send_email_reset_password(user, secret_key):
    token = generate_token(secret_key, user.k_number)
    sender = "no-reply@sbs.kcl.ac.uk"
    recipients = [str(user.k_number) + "@kcl.ac.uk"]
    subject = "Forgot my password"
    path = "http://localhost:5000/reset-password/"
    content = f"Please click on the following link to reset your password {path}{token}"

    send_email(sender, recipients, subject, content)
