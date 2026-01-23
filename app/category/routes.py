from flask import Blueprint, request, jsonify
from app import limiter
from app import db
from app.authentication.model import User
from datetime import datetime, timedelta
import secrets
from functools import wraps
from app.category.model import GlassCategory
from app.authentication.routes import owner_required
from flask_jwt_extended import jwt_required

from app.utilis.response import success_response, error_response

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/categories', methods=['GET'])
@jwt_required()

def get_categories():
    categories = GlassCategory.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'display_name': c.display_name,
        'price_per_sqm': c.price_per_sqm,
        'description': c.description
    } for c in categories])

@category_bp.route('/categories', methods=['POST'])
@owner_required

def create_category():
    data = request.get_json()
    
    category = GlassCategory(
        name=data['name'],
        display_name=data['display_name'],
        price_per_sqm=data['price_per_sqm'],
        description=data.get('description', '')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201
