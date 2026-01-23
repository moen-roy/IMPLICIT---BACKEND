from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime, timedelta
from functools import wraps
from app.system.model import SystemSettings, DiscountCode
from app.authentication.routes import owner_required
from flask_jwt_extended import jwt_required

system_bp = Blueprint('system', __name__, url_prefix='/system')

@system_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    settings = SystemSettings.query.all()
    return jsonify({s.setting_key: s.setting_value for s in settings})

@system_bp.route('/settings', methods=['PUT'])
@owner_required
def update_settings():
    data = request.get_json()
    
    for key, value in data.items():
        setting = SystemSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = str(value)
        else:
            setting = SystemSettings(setting_key=key, setting_value=str(value))
            db.session.add(setting)
    
    db.session.commit()
    return jsonify({'message': 'Settings updated'})

# ===== DISCOUNT CODES (Owner Only) =====

@system_bp.route('/discounts', methods=['GET'])
@jwt_required()
def get_discounts():
    discounts = DiscountCode.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': d.id,
        'code': d.code,
        'discount_percent': d.discount_percent
    } for d in discounts])

@system_bp.route('/discounts', methods=['POST'])
@owner_required
def create_discount():
    data = request.get_json()
    
    discount = DiscountCode(
        code=data['code'].upper(),
        discount_percent=data['discount_percent']
    )
    
    db.session.add(discount)
    db.session.commit()
    
    return jsonify({'message': 'Discount code created'}), 201

@system_bp.route('/discounts/<int:discount_id>', methods=['DELETE'])
@owner_required
def delete_discount(discount_id):
    discount = DiscountCode.query.get_or_404(discount_id)
    discount.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Discount code deleted'})