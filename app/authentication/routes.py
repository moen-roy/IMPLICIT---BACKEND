from flask import Blueprint, request, jsonify
from app import limiter
from app import db
from app.authentication.model import User
from datetime import datetime, timedelta
import secrets
from functools import wraps
from app.utilis.validation import validate_email, validate_password, validate_phone, require_json
from app.utilis.response import success_response, error_response
from flask_jwt_extended import (
    create_access_token,
     create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# =====================================
# REGISTER (User)
# =====================================
@auth_bp.route('/register', methods=['POST'])
# @limiter.limit("5 per hour")  # Only 5 registrations per hour per IP
@require_json

def register():
    try:
        data = request.get_json()

        # Extract data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = str(data.get('password', ''))
        phone_number = data.get('phone_number', '').strip() if data.get('phone_number') else None

        # Validate required fields
        if not all([username, email, password]):
            return error_response('Username, email, and password are required')

        # Validate email
        if not validate_email(email):
            return error_response('Invalid email format')

        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return error_response(msg)

        # Validate phone (if provided)
        if phone_number and not validate_phone(phone_number):
            return error_response('Invalid phone number format')
        
        if len(password) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }), 400

        # Check duplicates
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return error_response('Username or Email already exists')

        # Create user
        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Generate token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)


        return success_response(
            data={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            },
            message='Registration successful',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Registration failed: {str(e)}', status=500)

# =====================================
# LOGIN
# =====================================
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force

def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')


    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
  

    # Create a JWT access token that includes the user's role in claims.
    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            }
    }), 200


# =====================================
# FORGOT PASSWORD
# =====================================
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'message': 'Email is required'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user.reset_token = secrets.token_urlsafe(32)
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        # In production: email the reset token instead
        return jsonify({
            'message': 'Reset token generated successfully',
            'reset_token': user.reset_token
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to generate reset token: {str(e)}'}), 500


# =====================================
# RESET PASSWORD
# =====================================
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        password = str(data.get('password'))
        confirm_password = str(data.get('confirm_password'))

        if not token or not password or not confirm_password:
            return jsonify({'message': 'All fields are required'}), 400

        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'}), 400

        user = User.query.filter_by(reset_token=token).first()
        if not user:
            return jsonify({'message': 'Invalid token'}), 400

        if user.reset_token_expires < datetime.utcnow():
            return jsonify({'message': 'Reset token has expired'}), 400

        user.set_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()

        return jsonify({'message': 'Password reset successful'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Password reset failed: {str(e)}'}), 500






