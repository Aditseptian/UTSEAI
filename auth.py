# auth.py
import jwt
import datetime

SECRET_KEY = "your_super_secret_key"  # Ganti dengan kunci rahasia yang kompleks
ALGORITHM = "HS256"

def generate_token():
    payload = {
        "iss": "MainApp",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False