#!/usr/bin/env python3
"""
Flask Multi Store - Phiên bản hoạt động 100%
Không cần MySQL, chỉ cần Flask và SQLite
"""

import os
from flask import Flask, render_template_string, request, session, redirect, url_for, flash

# Tạo Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key-123'

# Dữ liệu mẫu trong memory (không cần database)
STORE_DATA = {
    'name': 'Cửa hàng Demo',
    'description': 'Cửa hàng bán đồ ăn và đồ uống ngon',
    'phone': '0123456789',
    'email': 'demo@store.com'
}

PRODUCTS = [
    {
        'id': 1,
        'name': 'Bánh mì thịt nướng',
        'price': 25000,
        'description': 'Bánh mì thịt nướng thơm ngon',
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop',
        'featured': True
    },
    {
        'id': 2,
        'name': 'Phở bò đặc biệt',
        'price': 45000,
        'description': 'Phở bò nước trong, thịt mềm',
        'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop',
        'featured': True
    },
    {
        'id': 3,
        'name': 'Cơm tấm sườn nướng',
        'price': 35000,
        'description': 'Cơm tấm sườn nướng đậm đà',
        'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop',
        'featured': True
    },
    {
        'id': 4,
        'name': 'Cà phê sữa đá',
        'price': 20000,
        'description': 'Cà phê sữa đá truyền thống',
        'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop',
        'featured': False
    },
    {
        'id': 5,
        'name': 'Trà sữa trân châu',
        'price': 30000,
        'description': 'Trà sữa trân châu ngọt ngào',
        'image': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop',
        'featured': False
    },
    {
        'id': 6,
        'name': 'Nước ép cam tươi',
        'price': 25000,
        'description': 'Nước ép cam tươi vitamin C',
        'image': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop',
        'featured': False
    }
]

# Template HTML
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ store.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        .product-card {
            transition: transform 0.2s;
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
        }
        .price {
            font-size: 1.2em;
            font-weight: bold;
            color: #e74c3c;
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5em;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand text-primary" href="{{ url_for('index') }}">
                <i class="fas fa-store me-2"></i>{{ store.name }}
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('cart') }}">
                    <i class="fas fa-shopping-cart me-1"></i>
                    Giỏ hàng 
                    <span class="badge bg-danger" id="cart-count">{{ cart_count }}</span>
                </a>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="container mt-3">
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Content -->
    {% block content %}{% endblock %}

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4 mt-5">
        <div class="container">
            <p>&copy; 2024 {{ store.name }}. Powered by Flask Multi Store</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

INDEX_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
<!-- Hero Section -->
<section class="hero-section">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">{{ store.name }}</h1>
        <p class="lead">{{ store.description }}</p>
        <p><i class="fas fa-phone me-2"></i>{{ store.phone }} | <i class="fas fa-envelope me-2"></i>{{ store.email }}</p>
    </div>
</section>

<!-- Featured Products -->
<div class="container my-5">
    <h2 class="text-center mb-5">
        <i class="fas fa-star text-warning me-2"></i>Sản phẩm nổi bật
    </h2>
    <div class="row">
        {% for product in featured_products %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card product-card h-100">
                <img src="{{ product.image }}" class="card-img-top" alt="{{ product.name }}" 
                     style="height: 250px; object-fit: cover;">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <p class="card-text text-muted flex-grow-1">{{ product.description }}</p>
                    <div class="price mb-3">{{ "{:,.0f}".format(product.price) }}đ</div>
                    <form method="POST" action="{{ url_for('add_to_cart') }}">
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

    <!-- All Products -->
    <h2 class="text-center mb-5 mt-5">
        <i class="fas fa-utensils text-info me-2"></i>Tất cả sản phẩm
    </h2>
    <div class="row">
        {% for product in all_products %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card product-card h-100">
                <img src="{{ product.image }}" class="card-img-top" alt="{{ product.name }}" 
                     style="height: 250px; object-fit: cover;">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <p class="card-text text-muted flex-grow-1">{{ product.description }}</p>
                    <div class="price mb-3">{{ "{:,.0f}".format(product.price) }}đ</div>
                    <form method="POST" action="{{ url_for('add_to_cart') }}">
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
{% endblock %}
'''

CART_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
<div class="container my-5">
    <h2 class="mb-4">
        <i class="fas fa-shopping-cart me-2"></i>Giỏ hàng của bạn
    </h2>
    
    {% if cart_items %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr>
                        <th>Sản phẩm</th>
                        <th>Hình ảnh</th>
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
                            <strong>{{ item.name }}</strong><br>
                            <small class="text-muted">{{ item.description }}</small>
                        </td>
                        <td>
                            <img src="{{ item.image }}" alt="{{ item.name }}" 
                                 style="width: 60px; height: 60px; object-fit: cover;" class="rounded">
                        </td>
                        <td>{{ item.quantity }}</td>
                        <td>{{ "{:,.0f}".format(item.price) }}đ</td>
                        <td class="fw-bold text-primary">{{ "{:,.0f}".format(item.total) }}đ</td>
                        <td>
                            <a href="{{ url_for('remove_from_cart', product_id=item.id) }}" 
                               class="btn btn-sm btn-outline-danger"
                               onclick="return confirm('Xóa sản phẩm này?')">
                                <i class="fas fa-trash"></i>
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr class="table-success">
                        <th colspan="4">Tổng cộng:</th>
                        <th class="text-primary">{{ "{:,.0f}".format(total) }}đ</th>
                        <th></th>
                    </tr>
                </tfoot>
            </table>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <a href="{{ url_for('index') }}" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>Tiếp tục mua hàng
                </a>
            </div>
            <div class="col-md-6 text-end">
                <button class="btn btn-success btn-lg">
                    <i class="fas fa-credit-card me-2"></i>Thanh toán ({{ "{:,.0f}".format(total) }}đ)
                </button>
            </div>
        </div>
    {% else %}
        <div class="text-center py-5">
            <i class="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
            <h3>Giỏ hàng trống</h3>
            <p class="text-muted mb-4">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
            <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg">
                <i class="fas fa-shopping-bag me-2"></i>Bắt đầu mua sắm
            </a>
        </div>
    {% endif %}
</div>
{% endblock %}
'''

# Helper functions
def get_product_by_id(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            return product
    return None

def get_cart_count():
    cart = session.get('cart', {})
    return sum(cart.values())

# Routes
@app.route('/')
def index():
    featured_products = [p for p in PRODUCTS if p['featured']]
    return render_template_string(INDEX_TEMPLATE, 
                                store=STORE_DATA,
                                featured_products=featured_products,
                                all_products=PRODUCTS,
                                cart_count=get_cart_count())

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = get_product_by_id(int(product_id))
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'description': product['description'],
                'image': product['image'],
                'price': product['price'],
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template_string(CART_TEMPLATE,
                                store=STORE_DATA,
                                cart_items=cart_items,
                                total=total,
                                cart_count=get_cart_count())

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id:
        flash('Sản phẩm không hợp lệ!', 'error')
        return redirect(url_for('index'))
    
    product = get_product_by_id(int(product_id))
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('index'))
    
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    flash(f'Đã thêm {product["name"]} vào giỏ hàng!', 'success')
    return redirect(url_for('index'))

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        product = get_product_by_id(product_id)
        del cart[str(product_id)]
        session['cart'] = cart
        flash(f'Đã xóa {product["name"] if product else "sản phẩm"} khỏi giỏ hàng!', 'success')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    print("🚀 Flask Multi Store - Working Version")
    print("=" * 50)
    print("✅ Không cần database - dùng dữ liệu trong memory")
    print("✅ Có ảnh đẹp từ Unsplash")
    print("✅ Chức năng giỏ hàng hoàn chỉnh")
    print("🌐 Truy cập: http://localhost:5000")
    print("🛒 Giỏ hàng: http://localhost:5000/cart")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 50)
    
    app.run(debug=True, port=5000)
