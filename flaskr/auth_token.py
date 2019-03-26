from itsdangerous import URLSafeTimedSerializer


def generate_token(secret_key, message):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps(message)
    return token


def verify_token(secret_key, token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        message = serializer.loads(token, max_age=expiration)
    except:
        return False
    return message
