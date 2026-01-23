from app.db import db
from datetime import datetime

class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.column(db.integer, primary_key= True)
    client_name =db.column(db.String(80), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items=db.column(nullable=False)
    subtotal=db.column(db.Float, default=0)
    tax_rate=db.column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    tax_amount=db.column(db.Float, default=0)
    shipping_cost=db.column(db.Float, default=0)
    total=db.column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






   