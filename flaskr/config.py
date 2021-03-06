from hashlib import sha3_256


class Config:
    SECRET_KEY = 'powerful secretkey'
    EMAIL_CONFIRMATION_EXPIRATION = 86400
    PASSWORD_RESET_EXPIRATION = 86400
    MESSAGE_SEPARATION_TOKEN = "[" + sha3_256(bytes(SECRET_KEY, "utf-8")).hexdigest() + "]"
    EMAIL_CONFIRMATION_REQUIRED = False
    BUDDY_LIMIT = 15
    WEBSITE_PATH = "http://ec2-34-254-100-139.eu-west-1.compute.amazonaws.com:5000/"
