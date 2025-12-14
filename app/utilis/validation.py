import re
from functools import wraps
from flask import jsonify, request

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?[0-9]{10,15}$')

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    return EMAIL_REGEX.match(email.strip()) is not None

def validate_password(password):
    """Validate password strength"""
    password = str(password).strip()
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter"
    return True, "Valid"

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True  # Phone is optional
    return PHONE_REGEX.match(phone.strip()) is not None

def require_json(f):
    """Decorator to ensure request has JSON body"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return jsonify({'success': False, 'message': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated