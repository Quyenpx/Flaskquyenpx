#!/usr/bin/env python3
"""
Quick start script - Chạy nhanh ứng dụng Flask với SQLite
"""

import os
import sys
from flask import Flask, render_template, g, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quick_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo database
db = SQLAlchemy(app)

# Models đơn giản
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

# Helper functions
def get_current_store():
    store_slug = request.args.get('store', 'demo')
    return Store.query.filter_by(slug=store_slug, is_active=True).first()

@app.before_request
def load_store():
    # Tự động tạo database nếu chưa có
    if not os.path.exists('quick_store.db'):
        with app.app_context():
            db.create_all()
            print("✅ Đã tạo database tự động")

    g.store = get_current_store()
    if not g.store and request.endpoint not in ['setup', 'create_templates']:
        return redirect(url_for('setup'))

@app.context_processor
def inject_store():
    return dict(current_store=getattr(g, 'store', None))

# Routes
@app.route('/setup')
def setup():
    """Setup dữ liệu mẫu"""
    try:
        db.create_all()
        
        # Kiểm tra đã có dữ liệu chưa
        if Store.query.first():
            return redirect(url_for('index', store='demo'))
        
        # Tạo store demo
        store = Store(
            name='Cửa hàng Demo',
            slug='demo',
            description='Cửa hàng demo',
            phone='0123456789',
            email='demo@example.com',
            address='123 ABC Street'
        )
        db.session.add(store)
        db.session.flush()
        
        # Tạo danh mục
        category = ProductCategory(
            store_id=store.id,
            name='Đồ ăn',
            slug='do-an',
            description='Các món ăn ngon'
        )
        db.session.add(category)
        db.session.flush()
        
        # Tạo sản phẩm
        products = [
            {'name': 'Bánh mì', 'price': 25000},
            {'name': 'Phở bò', 'price': 45000},
            {'name': 'Cơm tấm', 'price': 35000}
        ]
        
        for i, prod in enumerate(products):
            product = Product(
                store_id=store.id,
                category_id=category.id,
                name=prod['name'],
                slug=f'product-{i+1}',
                description=f'Mô tả {prod["name"]}',
                short_description=f'Ngon và rẻ',
                price=prod['price'],
                stock_quantity=100,
                is_featured=(i == 0)
            )
            db.session.add(product)
        
        db.session.commit()
        flash('Đã khởi tạo dữ liệu thành công!', 'success')
        return redirect(url_for('index', store='demo'))
        
    except Exception as e:
        return f"Lỗi setup: {str(e)}"

@app.route('/')
def index():
    """Trang chủ"""
    store = g.store
    
    categories = ProductCategory.query.filter_by(
        store_id=store.id, is_active=True
    ).order_by(ProductCategory.sort_order).all()
    
    featured_products = Product.query.filter_by(
        store_id=store.id, is_active=True, is_featured=True
    ).limit(6).all()
    
    latest_products = Product.query.filter_by(
        store_id=store.id, is_active=True
    ).order_by(Product.id.desc()).limit(6).all()
    
    return render_template('quick_index.html',
                         store=store,
                         categories=categories,
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
    
    return render_template('quick_cart.html',
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

# Template đơn giản
@app.route('/create-templates')
def create_templates():
    """Tạo templates cơ bản"""
    os.makedirs('templates', exist_ok=True)
    
    # Base template
    base_html = '''<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{{ current_store.name if current_store else 'Store' }}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --primary-color: {{ current_store.primary_color if current_store else '#007bff' }}; }
        .btn-primary { background-color: var(--primary-color); border-color: var(--primary-color); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index', store=current_store.slug if current_store else 'demo') }}">
                {{ current_store.name if current_store else 'Store' }}
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('cart', store=current_store.slug if current_store else 'demo') }}">
                    Giỏ hàng
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
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    # Index template
    index_html = '''{% extends "base.html" %}
{% block content %}
<h1>{{ store.name }}</h1>
<p>{{ store.description }}</p>

{% if featured_products %}
<h3>Sản phẩm nổi bật</h3>
<div class="row">
    {% for product in featured_products %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.short_description }}</p>
                <p class="text-primary fw-bold">{{ "{:,.0f}".format(product.current_price) }}đ</p>
                <form method="POST" action="{{ url_for('add_to_cart', store=store.slug) }}">
                    <input type="hidden" name="product_id" value="{{ product.id }}">
                    <button type="submit" class="btn btn-primary">Thêm vào giỏ</button>
                </form>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endif %}
{% endblock %}'''
    
    # Cart template
    cart_html = '''{% extends "base.html" %}
{% block content %}
<h2>Giỏ hàng</h2>
{% if cart_items %}
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr><th>Sản phẩm</th><th>Số lượng</th><th>Giá</th><th>Tổng</th></tr>
            </thead>
            <tbody>
                {% for item in cart_items %}
                <tr>
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ "{:,.0f}".format(item.product.current_price) }}đ</td>
                    <td>{{ "{:,.0f}".format(item.total) }}đ</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <h4>Tổng: {{ "{:,.0f}".format(cart_total) }}đ</h4>
{% else %}
    <p>Giỏ hàng trống</p>
{% endif %}
<a href="{{ url_for('index', store=current_store.slug) }}" class="btn btn-secondary">Tiếp tục mua</a>
{% endblock %}'''
    
    # Ghi files
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    with open('templates/quick_index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('templates/quick_cart.html', 'w', encoding='utf-8') as f:
        f.write(cart_html)
    
    return "Templates đã được tạo!"

if __name__ == '__main__':
    print("🚀 Quick Start Flask Multi Store")
    print("📝 Truy cập: http://localhost:5000/create-templates (tạo templates)")
    print("📝 Sau đó: http://localhost:5000/setup (khởi tạo dữ liệu)")
    print("🌐 Website: http://localhost:5000?store=demo")
    
    app.run(debug=True, port=5000)
