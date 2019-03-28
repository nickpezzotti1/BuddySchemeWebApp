import smtplib
from email.mime.text import MIMEText
from flaskr.auth_token import generate_token
from flask import current_app

COMMASPACE = ', '


def send_email(sender, recipients, subject, content):
    try:
        # Run a local instance of a email server that echoes
        # the messages on terminal
        # (env) $ python3 -m smtpd -c DebuggingServer -n localhost:1025
        server = smtplib.SMTP("localhost", 1025)

        msg = MIMEText(content)
        msg['From'] = sender
        msg['To'] = COMMASPACE.join(recipients)
        msg["Subject"] = subject

        server.send_message(msg)
        server.close()
    except Exception as e:
        print(e)


def send_email_confirmation_to_user(k_number, scheme_id, secret_key):
    message = str(k_number) + \
              current_app.config["MESSAGE_SEPARATION_TOKEN"] + \
              str(scheme_id)

    token = generate_token(secret_key=secret_key, message=message)
    sender = "no-reply@sbs.kcl.ac.uk"
    recipients = [str(k_number) + "@kcl.ac.uk"]
    subject = "Email Confirmation - Student Buddy System"
    path = current_app.config["WEBSITE_PATH"] + "confirm/"
    content = f"Welcome to KCL\'s Student Buddy System. \n Please activate your email at {path}{token}"

    send_email(sender, recipients, subject, content)


def send_email_reset_password(k_number, scheme_id, secret_key):
    message = str(k_number) + \
              current_app.config["MESSAGE_SEPARATION_TOKEN"] + \
              str(scheme_id)

    token = generate_token(secret_key=secret_key, message=message)
    sender = "no-reply@sbs.kcl.ac.uk"
    recipients = [k_number + "@kcl.ac.uk"]
    subject = "Forgot my password"
    path = current_app.config["WEBSITE_PATH"] + "forgot-my-password/"
    content = f"Please click on the following link to reset your password {path}{token}"

    send_email(sender, recipients, subject, content)

def send_email_scheme_feedback(k_numbers, feedback_url):
    sender = "no-reply@sbs.kcl.ac.uk"
    subject = "Student buddy scheme feedback"
    recipients = [(str(i) + "@kcl.ac.uk") for i in k_numbers]
    content = f"Your feedback is very important to us. Please click on the following link and let us know what can be done better next time! {feedback_url}"

    send_email(sender, recipients, subject, content)

def send_email_scheme_invite(email, token):

    sender = "no-reply@sbs.kcl.ac.uk"
    subject = "Student buddy scheme feedback"
    recipients = [email]
    path = current_app.config["WEBSITE_PATH"] + "signup/"
    content = f"You have been invited to join the KCL's new Student Buddy Scheme. Follow this link and register! {path}{token}"

    send_email(sender, recipients, subject, content)
