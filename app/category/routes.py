from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime, timedelta
from functools import wraps
from app.authentication.model import User
from app.category.model import GlassCategory
from app.authentication.routes import owner_required
from flask_jwt_extended import jwt_required, get_jwt_identity,


from app.utilis.response import success_response, error_response

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/categories', methods=['GET'])
@jwt_required()

def get_categories():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get categories based on user role
    if user.role == 'owner':
        # Owner sees their own categories
        categories = GlassCategory.query.filter_by(user_id=user_id, is_active=True).all()
    else:
        # Cashier sees categories from their owner
        categories = GlassCategory.query.filter_by(user_id=user_id, is_active=True).all()
        
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
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if category already exists for this user
    if GlassCategory.query.filter_by(user_id=user_id, name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 409
    
    
    category = GlassCategory(
        user_id=user_id,
        name=data['name'],
        display_name=data['display_name'],
        price_per_sqm=data['price_per_sqm'],
        description=data.get('description', '')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

@category_bp.route('/<int:category_id>', methods=['PUT'])
@owner_required
def update_category(category_id):
    user_id = get_jwt_identity()
    category = GlassCategory.query.filter_by(id=category_id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    category.display_name = data.get('display_name', category.display_name)
    category.price_per_sqm = data.get('price_per_sqm', category.price_per_sqm)
    category.description = data.get('description', category.description)
    
    db.session.commit()
    
    return jsonify({'message': 'Category updated'})


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@owner_required

def delete_category(category_id):
    user_id = get_jwt_identity()
    category = GlassCategory.query.filter_by(id=category_id, user_id=user_id).first_or_404()
    category.is_active = False  # Soft delete
    db.session.commit()
    
    return jsonify({'message': 'Category deleted'})
