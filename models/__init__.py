from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Khởi tạo database với Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import tất cả models để Flask-Migrate có thể detect
    from . import store, product, user, order
    
    return db
