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
    role = db.Column(db.String(20), default='cashier')  
    is_verified = db.Column(db.Boolean, default=False)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship (one-to-many)
    categories = db.relationship('GlassCategory', backref='owner', lazy=True, cascade='all, delete-orphan')
    discount_codes = db.relationship('DiscountCode', backref='owner', lazy=True, cascade='all, delete-orphan')
    quotes = db.relationship('Quote', backref='creator', lazy=True, cascade='all, delete-orphan')
    system_settings = db.relationship('SystemSettings', backref='owner', lazy=True, cascade='all, delete-orphan')
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

        