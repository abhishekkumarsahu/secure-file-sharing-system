from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt="email-verification")

def verify_token(token, max_age=3600):  # 1 hour expiry
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt="email-verification", max_age=max_age)
        return email
    except Exception:
        return None
    
def generate_file_token(file_id):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    return s.dumps(file_id, salt="file-download")

def verify_file_token(token, max_age=900):  # 15 minutes
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        file_id = s.loads(token, salt="file-download", max_age=max_age)
        return file_id
    except Exception:
        return None