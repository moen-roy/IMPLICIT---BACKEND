from flask import Flask
from flask_cors import CORS
import os
from app.config import Config
from app.db import db, migrate, jwt, bcrypt,limiter

from app.authentication.routes import auth_bp  
from app.category.routes import category_bp


def create_app():
    app = Flask(__name__)
    # Allow routes without a trailing slash to be accepted without a redirect.
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)  

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)

    limiter.init_app(app)

    add_routes(app)


    return app


#  tests routes for listing all routes
def add_routes(app):
    @app.route('/routes')
    def list_routes():
        return {
            "routes": [
                {
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule.rule)
                }
                for rule in app.url_map.iter_rules()
            ]
        }, 200  