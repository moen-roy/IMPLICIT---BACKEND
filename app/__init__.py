from flask import Flask
from flask_cors import CORS
import os
# from app.journals.routes import journal_bp  
from app.config import Config
from app.db import db, migrate, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    # Allow routes without a trailing slash to be accepted without a redirect.
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    
    # Register blueprints
    # app.register_blueprint( )   


#     # Import models for migrations
#     register_models()

#     # Add routes
#     # add_routes(app)

#     return app


# def register_models():
#     #Import models for Flask-Migrate
#     try:
#         from app.auth import models as auth_models  
#         from app.community import models as community_models
#         from app.journals import models as journals_models  
#         from app.mood import models as mood_models  
#     except ImportError:
#         pass

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