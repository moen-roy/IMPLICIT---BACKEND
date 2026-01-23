from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime, timedelta
from functools import wraps
from app.authentication.model import User
from app.quotation.model import Quote
from app.authentication.routes import owner_required
from flask_jwt_extended import jwt_required

quotation_bp = Blueprint('quotation', __name__, url_prefix='/quotation')    
@quotation_bp.route('/quotes', methods=['POST'])
@jwt_required()

def create_quote():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    quote = Quote(
        client_name=data['clientName'],
        created_by=user_id,
        items=data['items'],
        subtotal=data['subtotal'],
        discount_amount=data.get('discountAmount', 0),
        tax_amount=data.get('taxAmount', 0),
        shipping_cost=data.get('shippingCost', 0),
        total=data['total']
    )
    
    db.session.add(quote)
    db.session.commit()
    
    return jsonify({'message': 'Quote saved', 'id': quote.id}), 201

@quotation_bp.route('/quotes', methods=['GET'])
@jwt_required()
def get_quotes():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'owner':
        quotes = Quote.query.all()
    else:
        quotes = Quote.query.filter_by(created_by=user_id).all()
    
    return jsonify([{
        'id': q.id,
        'client_name': q.client_name,
        'total': q.total,
        'created_at': q.created_at.isoformat()
    } for q in quotes])
