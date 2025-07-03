#!/usr/bin/env python3
"""
Flask Multi Store - Phiên bản với templates riêng
Dễ dàng chỉnh sửa giao diện
"""

import os
from flask import Flask, render_template, session, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'easy-edit-store-key'

# Tạo thư mục templates và static
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Dữ liệu cửa hàng
STORES = {
    'demo': {
        'name': 'Cửa hàng Demo',
        'description': 'Đồ ăn và đồ uống ngon, giá rẻ',
        'logo': '🏪',
        'theme_color': '#007bff',
        'phone': '0123456789',
        'email': 'demo@store.com',
        'address': '123 Đường ABC, Quận XYZ, TP.HCM'
    }
}

PRODUCTS = [
    {'id': 1, 'name': 'Bánh mì thịt nướng', 'price': 25000, 'rating': 4.5, 'reviews': 128, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop', 'description': 'Bánh mì thịt nướng thơm ngon'},
    {'id': 2, 'name': 'Phở bò đặc biệt', 'price': 45000, 'rating': 4.8, 'reviews': 256, 'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop', 'description': 'Phở bò nước trong, thịt mềm'},
    {'id': 3, 'name': 'Cơm tấm sườn nướng', 'price': 35000, 'rating': 4.3, 'reviews': 89, 'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop', 'description': 'Cơm tấm sườn nướng đậm đà'},
    {'id': 4, 'name': 'Cà phê sữa đá', 'price': 20000, 'rating': 4.2, 'reviews': 167, 'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop', 'description': 'Cà phê sữa đá truyền thống'},
]

def create_templates():
    """Tạo các template files"""
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ store.name }}{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    
    <style>
        :root {
            --theme-color: {{ store.theme_color }};
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/" style="color: var(--theme-color);">
                {{ store.logo }} {{ store.name }}
            </a>
            
            <div class="navbar-nav ms-auto">
                <a class="nav-link position-relative" href="/cart">
                    <i class="fas fa-shopping-cart"></i> Giỏ hàng
                    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                        {{ cart_count }}
                    </span>
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

    <!-- Main Content -->
    {% block content %}{% endblock %}

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4 mt-5">
        <div class="container">
            <p>&copy; 2024 {{ store.name }}. Powered by Flask Multi Store</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>'''

    # Index template
    index_template = '''{% extends "base.html" %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">{{ store.logo }} {{ store.name }}</h1>
        <p class="lead fs-4">{{ store.description }}</p>
        <div class="row justify-content-center mt-4">
            <div class="col-md-8">
                <div class="store-info">
                    <div class="row">
                        <div class="col-md-4">
                            <i class="fas fa-phone text-primary"></i> {{ store.phone }}
                        </div>
                        <div class="col-md-4">
                            <i class="fas fa-envelope text-primary"></i> {{ store.email }}
                        </div>
                        <div class="col-md-4">
                            <i class="fas fa-map-marker-alt text-primary"></i> Địa chỉ
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Products -->
<div class="container my-5">
    <h2 class="text-center mb-5">
        <i class="fas fa-utensils text-primary me-2"></i>Sản phẩm của chúng tôi
    </h2>
    <div class="row">
        {% for product in products %}
        <div class="col-lg-3 col-md-6 mb-4">
            <div class="card product-card h-100">
                <div class="position-relative">
                    <img src="{{ product.image }}" class="card-img-top product-image" alt="{{ product.name }}">
                    <span class="position-absolute top-0 end-0 m-2 badge bg-warning text-dark">
                        ⭐ {{ product.rating }}
                    </span>
                </div>
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <p class="card-text text-muted flex-grow-1">{{ product.description }}</p>
                    <div class="rating mb-2">
                        {% for i in range(5) %}
                            {% if i < product.rating %}⭐{% else %}☆{% endif %}
                        {% endfor %}
                        ({{ product.reviews }} đánh giá)
                    </div>
                    <div class="price mb-3">{{ "{:,.0f}".format(product.price) }}đ</div>
                    <form method="POST" action="/add-to-cart" class="mt-auto">
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
{% endblock %}'''

    # Cart template
    cart_template = '''{% extends "base.html" %}

{% block content %}
<div class="container my-5">
    <h2 class="mb-4">🛒 Giỏ hàng của bạn</h2>
    
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
                            <strong>{{ item.product.name }}</strong><br>
                            <small class="text-muted">{{ item.product.description }}</small>
                        </td>
                        <td>
                            <img src="{{ item.product.image }}" style="width: 60px; height: 60px; object-fit: cover;" class="rounded">
                        </td>
                        <td>{{ item.quantity }}</td>
                        <td>{{ "{:,.0f}".format(item.product.price) }}đ</td>
                        <td class="fw-bold text-primary">{{ "{:,.0f}".format(item.total) }}đ</td>
                        <td>
                            <a href="/remove/{{ item.product.id }}" class="btn btn-sm btn-outline-danger"
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
                <a href="/" class="btn btn-outline-secondary btn-lg">
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
            <a href="/" class="btn btn-primary btn-lg">
                <i class="fas fa-shopping-bag me-2"></i>Bắt đầu mua sắm
            </a>
        </div>
    {% endif %}
</div>
{% endblock %}'''

    # CSS file
    css_content = '''/* Custom CSS cho Flask Multi Store */

/* Theme colors */
:root {
    --theme-color: #007bff;
    --secondary-color: #6c757d;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, var(--theme-color) 0%, #667eea 100%);
    color: white;
    padding: 80px 0;
}

.store-info {
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    padding: 20px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

/* Product cards */
.product-card {
    transition: all 0.3s ease;
    border: none;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-radius: 15px;
    overflow: hidden;
}

.product-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.product-image {
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.product-card:hover .product-image {
    transform: scale(1.05);
}

/* Buttons */
.btn-primary {
    background: var(--theme-color);
    border-color: var(--theme-color);
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background: var(--theme-color);
    border-color: var(--theme-color);
    opacity: 0.9;
    transform: translateY(-2px);
}

/* Price styling */
.price {
    font-size: 1.3em;
    font-weight: bold;
    color: var(--theme-color);
}

/* Rating stars */
.rating {
    color: #ffc107;
    font-size: 0.9em;
}

/* Navbar */
.navbar-brand {
    font-size: 1.5em;
    font-weight: bold;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.product-card {
    animation: fadeInUp 0.6s ease forwards;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-section {
        padding: 40px 0;
    }
    
    .display-4 {
        font-size: 2rem;
    }
    
    .store-info {
        padding: 15px;
    }
    
    .store-info .row > div {
        margin-bottom: 10px;
        text-align: center;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: var(--theme-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #0056b3;
}'''

    # JavaScript file
    js_content = '''// Custom JavaScript cho Flask Multi Store

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Product card animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = Math.random() * 0.3 + 's';
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.product-card').forEach(card => {
        observer.observe(card);
    });

    // Add to cart animation
    document.querySelectorAll('form[action="/add-to-cart"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang thêm...';
            button.disabled = true;
            
            // Reset after 1 second
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 1000);
        });
    });

    // Cart count animation
    function animateCartCount() {
        const cartBadge = document.querySelector('.badge');
        if (cartBadge) {
            cartBadge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 200);
        }
    }

    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

function showToast(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to page
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove after hiding
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}'''

    # Ghi các files
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_template)
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_template)
    
    with open('templates/cart.html', 'w', encoding='utf-8') as f:
        f.write(cart_template)
    
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    with open('static/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

def get_product_by_id(product_id):
    return next((p for p in PRODUCTS if p['id'] == product_id), None)

@app.context_processor
def inject_globals():
    cart_count = sum(session.get('cart', {}).values())
    return dict(
        store=STORES['demo'],
        cart_count=cart_count
    )

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

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
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
        flash('Đã thêm sản phẩm vào giỏ hàng!', 'success')
    return redirect(url_for('home'))

@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    print("🚀 Flask Multi Store - Template Version")
    print("=" * 50)
    print("✅ Templates riêng biệt - dễ chỉnh sửa")
    print("✅ CSS/JS files riêng")
    print("✅ Animations và effects")
    print("🌐 Truy cập: http://localhost:5000")
    print("📁 Files được tạo:")
    print("   - templates/base.html")
    print("   - templates/index.html") 
    print("   - templates/cart.html")
    print("   - static/css/style.css")
    print("   - static/js/main.js")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 50)
    
    # Tạo templates khi chạy
    create_templates()
    
    app.run(debug=True, port=5000, host='0.0.0.0')
