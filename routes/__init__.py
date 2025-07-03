from flask import Blueprint

def register_blueprints(app):
    """Đăng ký tất cả blueprints với Flask app"""
    
    # Import blueprints
    from .main import main_bp
    from .admin import admin_bp
    from .api import api_bp
    
    # Đăng ký blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
