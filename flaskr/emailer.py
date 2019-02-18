import smtplib
from email.mime.text import MIMEText

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
