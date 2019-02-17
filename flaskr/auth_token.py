from itsdangerous import URLSafeTimedSerializer

# TODO: include password salt
def generate_token(secret_key, k_number):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps(k_number)
    return token


def verify_token(secret_key, token, expiration=86400):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        k_number = serializer.loads(token, max_age=expiration)
    except:
        return False
    return k_number
