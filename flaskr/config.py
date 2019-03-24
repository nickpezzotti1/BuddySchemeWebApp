import os
from hashlib import sha3_256


class Config:
    SECRET_KEY = 'powerful secretkey'
    EMAIL_CONFIRMATION_EXPIRATION = 86400
    PASSWORD_RESET_EXPIRATION = 86400
    MESSAGE_SEPARATION_TOKEN = "[" + sha3_256(bytes(SECRET_KEY, "utf-8")).hexdigest() + "]"
