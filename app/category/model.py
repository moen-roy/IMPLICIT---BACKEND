from datetime import datetime
from app import db

class GlassCategory(db.Model):
    __tablename__ = 'glass_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # e.g., 'standard', 'tinted'
    display_name = db.Column(db.String(100), nullable=False)  # e.g., 'Standard Glass'
    price_per_sqm = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
