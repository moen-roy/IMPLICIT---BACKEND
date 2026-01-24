from app.db import db
from datetime import datetime

class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who created it
    client_name = db.Column(db.String(80), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items=db.Column(db.Text, nullable=False)
    subtotal=db.Column(db.Float, default=0)
    tax_rate=db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    tax_amount=db.Column(db.Float, default=0)
    shipping_cost=db.Column(db.Float, default=0)
    total=db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






   