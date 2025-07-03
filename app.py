#!/usr/bin/env python3
"""
Flask Multi Store - Railway Deploy Version
"""

import os
from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'railway-secret-2024')

# Dữ liệu sản phẩm trong memory
products = [
    {'id': 1, 'name': 'Bánh mì thịt nướng', 'price': 25000, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop', 'description': 'Bánh mì thịt nướng thơm ngon'},
    {'id': 2, 'name': 'Phở bò đặc biệt', 'price': 45000, 'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=300&h=200&fit=crop', 'description': 'Phở bò nước trong, thịt mềm'},
    {'id': 3, 'name': 'Cơm tấm sườn nướng', 'price': 35000, 'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=300&h=200&fit=crop', 'description': 'Cơm tấm sườn nướng đậm đà'},
    {'id': 4, 'name': 'Cà phê sữa đá', 'price': 20000, 'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300&h=200&fit=crop', 'description': 'Cà phê sữa đá truyền thống'},
]

@app.route('/')
def home():
    cart_count = sum(session.get('cart', {}).values())

    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏪 Cửa hàng Online</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .product-card {{ transition: transform 0.2s; border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .product-card:hover {{ transform: translateY(-5px); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold text-primary" href="/">🏪 Cửa hàng Online</a>
            <div class="navbar-nav ms-auto">
                <a href="/cart" class="btn btn-outline-primary position-relative">
                    🛒 Giỏ hàng <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">{cart_count}</span>
                </a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="container text-center">
            <h1 class="display-4 fw-bold mb-3">🏪 Cửa hàng Online</h1>
            <p class="lead">Đồ ăn ngon, giá rẻ, giao hàng nhanh chóng</p>
            <p>📞 0123456789 | 📧 contact@store.com</p>
        </div>
    </section>

    <div class="container my-5">
        <h2 class="text-center mb-5">🍽️ Sản phẩm của chúng tôi</h2>
        <div class="row">'''

    for product in products:
        html += f'''
            <div class="col-lg-3 col-md-6 mb-4">
                <div class="card product-card h-100">
                    <img src="{product['image']}" class="card-img-top" style="height: 200px; object-fit: cover;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{product['name']}</h5>
                        <p class="card-text text-muted flex-grow-1">{product['description']}</p>
                        <p class="text-primary fw-bold fs-5">{product['price']:,}đ</p>
                        <form method="POST" action="/add-to-cart" class="mt-auto">
                            <input type="hidden" name="product_id" value="{product['id']}">
                            <button type="submit" class="btn btn-primary w-100">🛒 Thêm vào giỏ</button>
                        </form>
                    </div>
                </div>
            </div>'''

    html += '''
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-4">
        <div class="container"><p>&copy; 2024 Cửa hàng Online. Powered by Flask</p></div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    return html
    
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
    
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
            total += item_total

    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛒 Giỏ hàng</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">🏪 Cửa hàng Online</a>
            <a href="/" class="btn btn-outline-secondary">← Quay lại</a>
        </div>
    </nav>

    <div class="container mt-4">
        <h2>🛒 Giỏ hàng của bạn</h2>'''

    if cart_items:
        html += '''<div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr><th>Sản phẩm</th><th>Hình ảnh</th><th>Số lượng</th><th>Đơn giá</th><th>Thành tiền</th><th>Thao tác</th></tr>
                </thead>
                <tbody>'''

        for item in cart_items:
            html += f'''<tr>
                <td><strong>{item['product']['name']}</strong><br><small class="text-muted">{item['product']['description']}</small></td>
                <td><img src="{item['product']['image']}" style="width: 50px; height: 50px; object-fit: cover;" class="rounded"></td>
                <td>{item['quantity']}</td>
                <td>{item['product']['price']:,}đ</td>
                <td class="fw-bold text-primary">{item['total']:,}đ</td>
                <td><a href="/remove/{item['product']['id']}" class="btn btn-sm btn-outline-danger" onclick="return confirm('Xóa sản phẩm này?')">🗑️</a></td>
            </tr>'''

        html += f'''</tbody>
                <tfoot>
                    <tr class="table-success">
                        <th colspan="4">Tổng cộng:</th>
                        <th class="text-primary">{total:,}đ</th>
                        <th></th>
                    </tr>
                </tfoot>
            </table>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <a href="/" class="btn btn-outline-secondary btn-lg">← Tiếp tục mua hàng</a>
            </div>
            <div class="col-md-6 text-end">
                <button class="btn btn-success btn-lg">💳 Thanh toán ({total:,}đ)</button>
            </div>
        </div>'''
    else:
        html += '''<div class="text-center py-5">
            <h3>🛒 Giỏ hàng trống</h3>
            <p class="text-muted">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
            <a href="/" class="btn btn-primary btn-lg">🛍️ Bắt đầu mua sắm</a>
        </div>'''

    html += '''</div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    return html

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
