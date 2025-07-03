#!/usr/bin/env python3
"""
Script để chạy ứng dụng Flask local với SQLite (không cần MySQL)
"""

import os
import sys
from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Tạo Flask app với cấu hình SQLite cho local development"""
    app = Flask(__name__)
    
    # Cấu hình cơ bản cho SQLite
    app.config['SECRET_KEY'] = 'dev-secret-key-for-local-testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_store.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['POSTS_PER_PAGE'] = 12
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600
    
    # Tạo thư mục upload
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Khởi tạo database
    from models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models để SQLAlchemy biết
    from models.store import Store
    from models.product import ProductCategory, Product
    from models.user import User
    from models.order import Order, OrderDetail
    
    # Đăng ký blueprints
    from routes.main import main_bp
    from routes.admin import admin_bp
    from routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Context processors
    @app.context_processor
    def inject_store():
        """Inject store info vào templates"""
        store = getattr(g, 'store', None)
        return dict(current_store=store)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # CLI command để khởi tạo dữ liệu
    @app.cli.command()
    def init_db():
        """Khởi tạo database với dữ liệu mẫu"""
        print("🔄 Đang tạo database...")
        
        # Tạo tables
        with app.app_context():
            db.create_all()
            
            # Kiểm tra xem đã có dữ liệu chưa
            existing_store = Store.query.filter_by(slug='demo').first()
            if existing_store:
                print("⚠️  Database đã có dữ liệu mẫu")
                return
            
            print("📝 Đang tạo dữ liệu mẫu...")
            
            # Tạo store demo
            demo_store = Store(
                name='Cửa hàng Demo',
                slug='demo',
                description='Cửa hàng demo cho hệ thống bán hàng đa tenant',
                phone='0123456789',
                email='demo@example.com',
                address='123 Đường ABC, Quận XYZ, TP.HCM',
                primary_color='#007bff',
                secondary_color='#6c757d'
            )
            db.session.add(demo_store)
            db.session.flush()
            
            # Tạo admin user
            admin_user = User(
                store_id=demo_store.id,
                username='admin',
                email='admin@demo.com',
                full_name='Quản trị viên',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            # Tạo danh mục
            categories_data = [
                {'name': 'Đồ ăn', 'slug': 'do-an', 'description': 'Các món ăn ngon'},
                {'name': 'Đồ uống', 'slug': 'do-uong', 'description': 'Các loại đồ uống'},
                {'name': 'Tráng miệng', 'slug': 'trang-mieng', 'description': 'Món tráng miệng'}
            ]
            
            for i, cat_data in enumerate(categories_data):
                category = ProductCategory(
                    store_id=demo_store.id,
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    description=cat_data['description'],
                    sort_order=i
                )
                db.session.add(category)
                db.session.flush()
                
                # Tạo sản phẩm cho mỗi danh mục
                products_data = [
                    {'name': f'{cat_data["name"]} số 1', 'price': 50000, 'description': 'Sản phẩm chất lượng cao'},
                    {'name': f'{cat_data["name"]} số 2', 'price': 75000, 'description': 'Sản phẩm được yêu thích'},
                    {'name': f'{cat_data["name"]} số 3', 'price': 100000, 'description': 'Sản phẩm cao cấp'}
                ]
                
                for j, prod_data in enumerate(products_data):
                    product = Product(
                        store_id=demo_store.id,
                        category_id=category.id,
                        name=prod_data['name'],
                        slug=f"{cat_data['slug']}-{j+1}",
                        description=prod_data['description'],
                        short_description=f'Mô tả ngắn cho {prod_data["name"]}',
                        price=prod_data['price'],
                        stock_quantity=100,
                        sort_order=j,
                        is_featured=(j == 0)  # Sản phẩm đầu tiên là featured
                    )
                    db.session.add(product)
            
            db.session.commit()
            print('✅ Đã khởi tạo database thành công!')
            print('🔑 Tài khoản admin: admin / admin123')
            print('🏪 Store demo: http://localhost:5000?store=demo')
    
    return app

def main():
    """Hàm chính để chạy ứng dụng"""
    print("🚀 Đang khởi động Flask Multi Store...")
    
    app = create_app()
    
    # Kiểm tra database
    with app.app_context():
        from models import db
        from models.store import Store
        
        # Tạo database nếu chưa có
        if not os.path.exists('local_store.db'):
            print("📦 Database chưa tồn tại, đang tạo...")
            db.create_all()
            
            # Chạy init_db command
            from flask.cli import with_appcontext
            init_db_func = app.cli.commands['init-db'].callback
            init_db_func()
        else:
            print("✅ Database đã tồn tại")
    
    print("🌐 Ứng dụng đang chạy tại:")
    print("   - Website: http://localhost:5000?store=demo")
    print("   - Admin: http://localhost:5000/admin?store=demo")
    print("   - API: http://localhost:5000/api")
    print("📝 Tài khoản admin: admin / admin123")
    print("🛑 Nhấn Ctrl+C để dừng")
    
    # Chạy app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
