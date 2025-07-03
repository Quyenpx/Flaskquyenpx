#!/usr/bin/env python3
"""
Script đơn giản nhất để chạy Flask Multi Store
Tự động tạo database và dữ liệu mẫu
"""

import os
from flask import Flask, render_template, g, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Tạo Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-for-demo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo database
db = SQLAlchemy(app)

# Models
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    primary_color = db.Column(db.String(7), default='#007bff')
    is_active = db.Column(db.Boolean, default=True)

class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2))
    stock_quantity = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price

# Tạo templates trong memory
def create_templates():
    """Tạo templates cần thiết"""
    os.makedirs('templates', exist_ok=True)
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ current_store.name if current_store else 'Multi Store' }}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: {{ current_store.primary_color if current_store else '#007bff' }};
        }
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        .text-primary {
            color: var(--primary-color) !important;
        }
        .product-card {
            transition: transform 0.2s;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .product-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{{ url_for('index', store=current_store.slug if current_store else 'demo') }}">
                <i class="fas fa-store me-2"></i>{{ current_store.name if current_store else 'Multi Store' }}
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('cart', store=current_store.slug if current_store else 'demo') }}">
                    <i class="fas fa-shopping-cart me-1"></i>Giỏ hàng
                    <span class="badge bg-primary ms-1" id="cart-count" style="display: none;">0</span>
                </a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container text-center">
            <p>&copy; 2024 {{ current_store.name if current_store else 'Multi Store' }}. Powered by Flask.</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Update cart count
        function updateCartCount() {
            const cartItems = JSON.parse(sessionStorage.getItem('cartCount') || '0');
            const badge = document.getElementById('cart-count');
            if (cartItems > 0) {
                badge.textContent = cartItems;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        }
        document.addEventListener('DOMContentLoaded', updateCartCount);
    </script>
</body>
</html>'''
    
    # Index template với ảnh từ internet
    index_template = '''{% extends "base.html" %}
{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <div class="bg-primary text-white text-center py-5 rounded">
            <h1 class="display-4 fw-bold">{{ store.name }}</h1>
            <p class="lead">{{ store.description }}</p>
        </div>
    </div>
</div>

{% if featured_products %}
<div class="row mb-5">
    <div class="col-12">
        <h2 class="mb-4"><i class="fas fa-star text-warning me-2"></i>Sản phẩm nổi bật</h2>
        <div class="row">
            {% for product in featured_products %}
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card product-card h-100">
                    {% set food_images = [
                        'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop'
                    ] %}
                    <img src="{{ food_images[loop.index0 % food_images|length] }}"
                         class="card-img-top" alt="{{ product.name }}"
                         style="height: 200px; object-fit: cover;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text text-muted flex-grow-1">{{ product.short_description }}</p>
                        <div class="price mb-3">
                            {% if product.is_on_sale %}
                                <span class="text-danger fw-bold">{{ "{:,.0f}".format(product.sale_price) }}đ</span>
                                <span class="text-muted text-decoration-line-through ms-2">{{ "{:,.0f}".format(product.price) }}đ</span>
                            {% else %}
                                <span class="text-primary fw-bold">{{ "{:,.0f}".format(product.price) }}đ</span>
                            {% endif %}
                        </div>
                        <form method="POST" action="{{ url_for('add_to_cart', store=store.slug) }}">
                            <input type="hidden" name="product_id" value="{{ product.id }}">
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="fas fa-cart-plus me-2"></i>Thêm vào giỏ
                            </button>
                        </form>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}

{% if latest_products %}
<div class="row">
    <div class="col-12">
        <h2 class="mb-4"><i class="fas fa-clock text-info me-2"></i>Sản phẩm mới nhất</h2>
        <div class="row">
            {% for product in latest_products %}
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card product-card h-100">
                    {% set drink_images = [
                        'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1571091655789-405eb7a3a3a8?w=400&h=300&fit=crop',
                        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop'
                    ] %}
                    <img src="{{ drink_images[loop.index0 % drink_images|length] }}"
                         class="card-img-top" alt="{{ product.name }}"
                         style="height: 200px; object-fit: cover;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text text-muted flex-grow-1">{{ product.short_description }}</p>
                        <div class="price mb-3">
                            <span class="text-primary fw-bold">{{ "{:,.0f}".format(product.current_price) }}đ</span>
                        </div>
                        <form method="POST" action="{{ url_for('add_to_cart', store=store.slug) }}">
                            <input type="hidden" name="product_id" value="{{ product.id }}">
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="fas fa-cart-plus me-2"></i>Thêm vào giỏ
                            </button>
                        </form>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}
{% endblock %}'''
    
    # Cart template
    cart_template = '''{% extends "base.html" %}
{% block content %}
<h2><i class="fas fa-shopping-cart me-2"></i>Giỏ hàng</h2>

{% if cart_items %}
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Sản phẩm</th>
                    <th>Số lượng</th>
                    <th>Đơn giá</th>
                    <th>Thành tiền</th>
                    <th>Thao tác</th>
                </tr>
            </thead>
            <tbody>
                {% for item in cart_items %}
                <tr>
                    <td>
                        <strong>{{ item.product.name }}</strong><br>
                        <small class="text-muted">{{ item.product.short_description }}</small>
                    </td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ "{:,.0f}".format(item.product.current_price) }}đ</td>
                    <td class="fw-bold text-primary">{{ "{:,.0f}".format(item.total) }}đ</td>
                    <td>
                        <a href="{{ url_for('remove_from_cart', product_id=item.product.id, store=current_store.slug) }}" 
                           class="btn btn-sm btn-outline-danger"
                           onclick="return confirm('Xóa sản phẩm này?')">
                            <i class="fas fa-trash"></i>
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="3">Tổng cộng:</th>
                    <th class="text-primary">{{ "{:,.0f}".format(cart_total) }}đ</th>
                    <th></th>
                </tr>
            </tfoot>
        </table>
    </div>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <a href="{{ url_for('index', store=current_store.slug) }}" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-left me-2"></i>Tiếp tục mua hàng
            </a>
        </div>
        <div class="col-md-6 text-end">
            <button class="btn btn-success btn-lg">
                <i class="fas fa-credit-card me-2"></i>Thanh toán
            </button>
        </div>
    </div>
{% else %}
    <div class="text-center py-5">
        <i class="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
        <h3>Giỏ hàng trống</h3>
        <p class="text-muted mb-4">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
        <a href="{{ url_for('index', store=current_store.slug) }}" class="btn btn-primary">
            <i class="fas fa-shopping-bag me-2"></i>Bắt đầu mua sắm
        </a>
    </div>
{% endif %}
{% endblock %}'''
    
    # Ghi files
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_template)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_template)
    with open('templates/cart.html', 'w', encoding='utf-8') as f:
        f.write(cart_template)

def init_database():
    """Khởi tạo database và dữ liệu mẫu"""
    with app.app_context():
        # Tạo tables
        db.create_all()
        
        # Kiểm tra đã có dữ liệu chưa
        if Store.query.first():
            return False
        
        # Tạo store demo
        store = Store(
            name='Cửa hàng Demo',
            slug='demo',
            description='Cửa hàng demo cho hệ thống bán hàng đa tenant',
            phone='0123456789',
            email='demo@example.com',
            address='123 Đường ABC, Quận XYZ, TP.HCM'
        )
        db.session.add(store)
        db.session.flush()
        
        # Tạo danh mục
        categories = [
            {'name': 'Đồ ăn', 'slug': 'do-an', 'description': 'Các món ăn ngon'},
            {'name': 'Đồ uống', 'slug': 'do-uong', 'description': 'Các loại đồ uống'},
            {'name': 'Tráng miệng', 'slug': 'trang-mieng', 'description': 'Món tráng miệng'}
        ]
        
        for i, cat_data in enumerate(categories):
            category = ProductCategory(
                store_id=store.id,
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=cat_data['description'],
                sort_order=i
            )
            db.session.add(category)
            db.session.flush()
            
            # Tạo sản phẩm cho mỗi danh mục
            products = [
                {'name': f'{cat_data["name"]} số 1', 'price': 50000, 'featured': True},
                {'name': f'{cat_data["name"]} số 2', 'price': 75000, 'featured': False},
                {'name': f'{cat_data["name"]} số 3', 'price': 100000, 'featured': False}
            ]
            
            for j, prod_data in enumerate(products):
                product = Product(
                    store_id=store.id,
                    category_id=category.id,
                    name=prod_data['name'],
                    slug=f"{cat_data['slug']}-{j+1}",
                    description=f'Mô tả chi tiết cho {prod_data["name"]}. Sản phẩm chất lượng cao, được chế biến từ nguyên liệu tươi ngon.',
                    short_description=f'Ngon, bổ, rẻ - {prod_data["name"]}',
                    price=prod_data['price'],
                    stock_quantity=100,
                    sort_order=j,
                    is_featured=prod_data['featured']
                )
                db.session.add(product)
        
        db.session.commit()
        return True

# Helper functions
def get_current_store():
    store_slug = request.args.get('store', 'demo')
    return Store.query.filter_by(slug=store_slug, is_active=True).first()

@app.context_processor
def inject_store():
    return dict(current_store=getattr(g, 'store', None))

@app.before_request
def load_store():
    g.store = get_current_store()

# Routes
@app.route('/')
def index():
    """Trang chủ"""
    store = g.store
    if not store:
        return "Store not found. Please visit: <a href='/setup'>Setup</a>"
    
    featured_products = Product.query.filter_by(
        store_id=store.id, is_active=True, is_featured=True
    ).limit(6).all()
    
    latest_products = Product.query.filter_by(
        store_id=store.id, is_active=True
    ).order_by(Product.id.desc()).limit(6).all()
    
    return render_template('index.html',
                         store=store,
                         featured_products=featured_products,
                         latest_products=latest_products)

@app.route('/cart')
def cart():
    """Giỏ hàng"""
    cart_items = session.get('cart', {})
    cart_data = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = float(product.current_price) * quantity
            cart_data.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html',
                         cart_items=cart_data,
                         cart_total=total)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Thêm vào giỏ hàng"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    flash('Đã thêm vào giỏ hàng!', 'success')
    return redirect(request.referrer or url_for('index', store=g.store.slug))

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    """Xóa khỏi giỏ hàng"""
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    return redirect(url_for('cart', store=g.store.slug))

@app.route('/setup')
def setup():
    """Setup dữ liệu"""
    try:
        create_templates()
        if init_database():
            flash('Đã khởi tạo dữ liệu thành công!', 'success')
        else:
            flash('Dữ liệu đã tồn tại!', 'info')
        return redirect(url_for('index', store='demo'))
    except Exception as e:
        return f"Lỗi setup: {str(e)}"

if __name__ == '__main__':
    print("🚀 Flask Multi Store - Simple Version")
    print("=" * 50)
    
    # Tự động setup
    if not os.path.exists('simple_store.db'):
        print("📦 Đang khởi tạo database...")
        create_templates()
        init_database()
        print("✅ Đã khởi tạo thành công!")
    
    print("🌐 Ứng dụng đang chạy tại:")
    print("   👉 http://localhost:5000?store=demo")
    print("   🛒 http://localhost:5000/cart?store=demo")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 50)
    
    app.run(debug=True, port=5000)
