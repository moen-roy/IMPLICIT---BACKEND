from app.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(50),nullable=False)  
    is_verified = db.Column(db.Boolean, default=False)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship (one-to-one)
    # therapist_profile = db.relationship("Therapist", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_personal(self):
        """Return True if the account_type is 'personal'."""
        return (self.account_type or '').lower() == 'personal'

    def promote_to_business(self):
        """Promote this account_type to business account."""
        self.account_type = 'business'

    def demote_to_personal(self):
        """Demote this account_type to a normal 'personal' account."""
        self.account_type = 'personal'
    
class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(10), nullable=True)
    currency = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)