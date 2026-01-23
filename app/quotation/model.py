from app.db import db
from datetime import datetime

class Quotation(db.Model):
    __tablename__ = 'quotation'

    id = db.column(db.integer, primary_key= True)
    client_name =db.column(db.String(80), nullable=False)
    company_no = db.Column(db.Integer, db.ForeignKey('users.phone_number'), nullable=False)
    items=db.column(nullable=False)
    subtotal=db.column(db.float(10,2), default=0)
    shipping_cost=db.column(db.float(10,2), default=0)
    tax_amount=db.column(db.float(10,2), default=0)
    total=db.column(db.float(10,2), default=0, nullable=False)
    tax_rate=db.column(db.float(5,2), default=0)
    discount_code=db.column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






   