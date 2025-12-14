from flask import jsonify

def success_response(data=None, message="Success", status=200):
    """Standard success response"""
    response = {
        'success': True,
        'message': message
    }
    if data:
        response['data'] = data
    return jsonify(response), status

def error_response(message="Error occurred", status=400, errors=None):
    """Standard error response"""
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status