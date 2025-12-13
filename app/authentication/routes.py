from flask import Blueprint, request, jsonify
from app import db
from app.authentication.model import User
from datetime import datetime, timedelta
import secrets
from functools import wraps
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# =====================================
# REGISTER (User)
# =====================================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    account_type = data.get('account_type')
    phone_number = data.get('phone_number')

    # Validation
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({'message': 'Username or Email already exists'}), 400

    # Create base user
    user = User(
        username=username,
        email=email,
        phone_number=phone_number,
        account_type=account_type
    )
    user.set_password(password)

    db.session.add(user)
    db.session.flush()  # So we can get user.id before committing    
    db.session.commit()  # Actually save to database


    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'account_type': user.account_type,
            'created_at': user.created_at
        }
    }), 201


# =====================================
# LOGIN
# =====================================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    account_type = data.get('account_type')
    password = data.get('password')


    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
  

    # Create a JWT access token that includes the user's role in claims.
    access_token = create_access_token(identity=user.id, additional_claims={"account_type": user.account_type})

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'account_type': user.account_type
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






