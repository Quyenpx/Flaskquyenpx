import os
from flask import Flask, render_template, g
from config import config
from models import init_db
from routes import register_blueprints

def create_app(config_name=None):
    """Factory function để tạo Flask app"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Khởi tạo database
    init_db(app)
    
    # Đăng ký blueprints
    register_blueprints(app)
    
    # Tạo thư mục upload nếu chưa có
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Context processors để inject biến vào templates
    @app.context_processor
    def inject_store():
        """Inject store info vào tất cả templates"""
        store = getattr(g, 'store', None)
        return dict(current_store=store)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # CLI commands
    @app.cli.command()
    def init_db_command():
        """Khởi tạo database với dữ liệu mẫu"""
        from models import db
        from models.store import Store
        from models.product import ProductCategory, Product
        from models.user import User
        
        # Tạo tables
        db.create_all()
        
        # Tạo store mẫu
        demo_store = Store.query.filter_by(slug='demo').first()
        if not demo_store:
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
            
            # Tạo danh mục mẫu
            categories = [
                {'name': 'Đồ ăn', 'slug': 'do-an', 'description': 'Các món ăn ngon'},
                {'name': 'Đồ uống', 'slug': 'do-uong', 'description': 'Các loại đồ uống'},
                {'name': 'Tráng miệng', 'slug': 'trang-mieng', 'description': 'Món tráng miệng'}
            ]
            
            for i, cat_data in enumerate(categories):
                category = ProductCategory(
                    store_id=demo_store.id,
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    description=cat_data['description'],
                    sort_order=i
                )
                db.session.add(category)
                db.session.flush()
                
                # Tạo sản phẩm mẫu cho mỗi danh mục
                products = [
                    {'name': f'{cat_data["name"]} 1', 'price': 50000},
                    {'name': f'{cat_data["name"]} 2', 'price': 75000},
                    {'name': f'{cat_data["name"]} 3', 'price': 100000}
                ]
                
                for j, prod_data in enumerate(products):
                    product = Product(
                        store_id=demo_store.id,
                        category_id=category.id,
                        name=prod_data['name'],
                        slug=f"{cat_data['slug']}-{j+1}",
                        description=f'Mô tả chi tiết cho {prod_data["name"]}',
                        short_description=f'Mô tả ngắn cho {prod_data["name"]}',
                        price=prod_data['price'],
                        stock_quantity=100,
                        sort_order=j,
                        is_featured=(j == 0)  # Sản phẩm đầu tiên là featured
                    )
                    db.session.add(product)
            
            db.session.commit()
            print('✅ Đã khởi tạo database với dữ liệu mẫu')
            print('🔑 Tài khoản admin: admin / admin123')
            print('🏪 Store demo: http://localhost:5000?store=demo')
        else:
            print('⚠️  Database đã được khởi tạo trước đó')
    
    @app.cli.command()
    def create_store():
        """Tạo store mới"""
        from models import db
        from models.store import Store
        from models.user import User
        
        name = input('Tên cửa hàng: ')
        slug = input('Slug (URL): ')
        email = input('Email: ')
        phone = input('Số điện thoại: ')
        address = input('Địa chỉ: ')
        
        # Kiểm tra slug trùng
        existing = Store.query.filter_by(slug=slug).first()
        if existing:
            print('❌ Slug đã tồn tại')
            return
        
        store = Store(
            name=name,
            slug=slug,
            email=email,
            phone=phone,
            address=address
        )
        db.session.add(store)
        db.session.flush()
        
        # Tạo admin user cho store
        admin_username = input('Username admin: ')
        admin_password = input('Password admin: ')
        admin_email = input('Email admin: ')
        
        admin_user = User(
            store_id=store.id,
            username=admin_username,
            email=admin_email,
            full_name='Quản trị viên',
            role='admin'
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        
        db.session.commit()
        print(f'✅ Đã tạo store: {name}')
        print(f'🔗 URL: http://localhost:5000?store={slug}')
        print(f'👤 Admin: {admin_username} / {admin_password}')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
