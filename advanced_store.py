#!/usr/bin/env python3
"""
Flask Multi Store - Phiên bản nâng cao
Có menu, phân trang, đánh giá, multi-store
"""

from flask import Flask, session, request, redirect, url_for, jsonify
import math
import random

app = Flask(__name__)
app.secret_key = 'advanced-store-key-123'

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
    },
    'coffee': {
        'name': 'Coffee House',
        'description': 'Cà phê ngon, không gian ấm cúng',
        'logo': '☕',
        'theme_color': '#8B4513',
        'phone': '0987654321',
        'email': 'coffee@house.com',
        'address': '456 Coffee Street, District 1, HCMC'
    },
    'restaurant': {
        'name': 'Nhà hàng Việt',
        'description': 'Món Việt truyền thống, hương vị đậm đà',
        'logo': '🍜',
        'theme_color': '#dc3545',
        'phone': '0369852147',
        'email': 'info@nhahanviet.com',
        'address': '789 Nguyễn Huệ, Quận 1, TP.HCM'
    }
}

# Danh mục sản phẩm
CATEGORIES = {
    'demo': [
        {'id': 1, 'name': 'Đồ ăn', 'icon': '🍽️'},
        {'id': 2, 'name': 'Đồ uống', 'icon': '🥤'},
        {'id': 3, 'name': 'Tráng miệng', 'icon': '🍰'}
    ],
    'coffee': [
        {'id': 1, 'name': 'Cà phê', 'icon': '☕'},
        {'id': 2, 'name': 'Trà', 'icon': '🍵'},
        {'id': 3, 'name': 'Bánh ngọt', 'icon': '🧁'}
    ],
    'restaurant': [
        {'id': 1, 'name': 'Món chính', 'icon': '🍜'},
        {'id': 2, 'name': 'Khai vị', 'icon': '🥗'},
        {'id': 3, 'name': 'Đồ uống', 'icon': '🍹'}
    ]
}

# Sản phẩm theo cửa hàng
PRODUCTS = {
    'demo': [
        {'id': 1, 'name': 'Bánh mì thịt nướng', 'price': 25000, 'category_id': 1, 'rating': 4.5, 'reviews': 128, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop', 'description': 'Bánh mì thịt nướng thơm ngon, giòn rụm'},
        {'id': 2, 'name': 'Phở bò đặc biệt', 'price': 45000, 'category_id': 1, 'rating': 4.8, 'reviews': 256, 'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop', 'description': 'Phở bò nước trong, thịt mềm, hương vị đậm đà'},
        {'id': 3, 'name': 'Cơm tấm sườn nướng', 'price': 35000, 'category_id': 1, 'rating': 4.3, 'reviews': 89, 'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop', 'description': 'Cơm tấm sườn nướng đậm đà hương vị'},
        {'id': 4, 'name': 'Cà phê sữa đá', 'price': 20000, 'category_id': 2, 'rating': 4.2, 'reviews': 167, 'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop', 'description': 'Cà phê sữa đá truyền thống Việt Nam'},
        {'id': 5, 'name': 'Trà sữa trân châu', 'price': 30000, 'category_id': 2, 'rating': 4.6, 'reviews': 203, 'image': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop', 'description': 'Trà sữa trân châu ngọt ngào, thơm mát'},
        {'id': 6, 'name': 'Nước ép cam tươi', 'price': 25000, 'category_id': 2, 'rating': 4.1, 'reviews': 94, 'image': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop', 'description': 'Nước ép cam tươi 100%, giàu vitamin C'},
        {'id': 7, 'name': 'Bánh flan', 'price': 15000, 'category_id': 3, 'rating': 4.4, 'reviews': 76, 'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=300&fit=crop', 'description': 'Bánh flan mềm mịn, ngọt dịu'},
        {'id': 8, 'name': 'Chè ba màu', 'price': 18000, 'category_id': 3, 'rating': 4.0, 'reviews': 52, 'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop', 'description': 'Chè ba màu truyền thống, mát lạnh'},
    ],
    'coffee': [
        {'id': 1, 'name': 'Espresso', 'price': 35000, 'category_id': 1, 'rating': 4.7, 'reviews': 145, 'image': 'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop', 'description': 'Espresso đậm đà, hương vị chuẩn Ý'},
        {'id': 2, 'name': 'Cappuccino', 'price': 45000, 'category_id': 1, 'rating': 4.6, 'reviews': 198, 'image': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&h=300&fit=crop', 'description': 'Cappuccino với lớp foam mịn màng'},
        {'id': 3, 'name': 'Latte Art', 'price': 50000, 'category_id': 1, 'rating': 4.8, 'reviews': 267, 'image': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop', 'description': 'Latte với nghệ thuật vẽ trên bọt sữa'},
        {'id': 4, 'name': 'Trà xanh matcha', 'price': 40000, 'category_id': 2, 'rating': 4.5, 'reviews': 123, 'image': 'https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=400&h=300&fit=crop', 'description': 'Trà xanh matcha Nhật Bản nguyên chất'},
        {'id': 5, 'name': 'Croissant bơ', 'price': 25000, 'category_id': 3, 'rating': 4.3, 'reviews': 87, 'image': 'https://images.unsplash.com/photo-1555507036-ab794f4afe5a?w=400&h=300&fit=crop', 'description': 'Croissant bơ giòn tan, thơm ngon'},
        {'id': 6, 'name': 'Tiramisu', 'price': 55000, 'category_id': 3, 'rating': 4.9, 'reviews': 234, 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop', 'description': 'Tiramisu Ý chính gốc, vị ngọt đắng hài hòa'},
    ],
    'restaurant': [
        {'id': 1, 'name': 'Bún bò Huế', 'price': 55000, 'category_id': 1, 'rating': 4.7, 'reviews': 189, 'image': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop', 'description': 'Bún bò Huế cay nồng, đậm đà hương vị cố đô'},
        {'id': 2, 'name': 'Bánh xèo miền Tây', 'price': 45000, 'category_id': 1, 'rating': 4.5, 'reviews': 156, 'image': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=400&h=300&fit=crop', 'description': 'Bánh xèo giòn rụm, nhân tôm thịt đầy đặn'},
        {'id': 3, 'name': 'Gỏi cuốn tôm thịt', 'price': 35000, 'category_id': 2, 'rating': 4.4, 'reviews': 98, 'image': 'https://images.unsplash.com/photo-1559314809-0f31657def5e?w=400&h=300&fit=crop', 'description': 'Gỏi cuốn tươi ngon với tôm thịt và rau thơm'},
        {'id': 4, 'name': 'Nước mía tươi', 'price': 15000, 'category_id': 3, 'rating': 4.2, 'reviews': 67, 'image': 'https://images.unsplash.com/photo-1546173159-315724a31696?w=400&h=300&fit=crop', 'description': 'Nước mía tươi mát, ngọt tự nhiên'},
    ]
}

def get_store_data(store_slug):
    """Lấy thông tin cửa hàng"""
    return STORES.get(store_slug, STORES['demo'])

def get_products_by_store(store_slug, category_id=None, page=1, per_page=6):
    """Lấy sản phẩm theo cửa hàng với phân trang"""
    products = PRODUCTS.get(store_slug, PRODUCTS['demo'])
    
    if category_id:
        products = [p for p in products if p['category_id'] == category_id]
    
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'products': products[start:end],
        'total': total,
        'pages': math.ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < math.ceil(total / per_page)
    }

def render_stars(rating):
    """Render sao đánh giá"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = '⭐' * full_stars
    if half_star:
        stars += '⭐'  # Có thể dùng ⭐ cho half star
    stars += '☆' * empty_stars
    
    return stars

@app.route('/')
@app.route('/<store_slug>')
def home(store_slug='demo'):
    store = get_store_data(store_slug)
    categories = CATEGORIES.get(store_slug, CATEGORIES['demo'])
    
    # Lấy tham số
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)
    
    # Lấy sản phẩm với phân trang
    products_data = get_products_by_store(store_slug, category_id, page)
    
    # Sản phẩm nổi bật (rating cao nhất)
    all_products = PRODUCTS.get(store_slug, PRODUCTS['demo'])
    featured_products = sorted(all_products, key=lambda x: x['rating'], reverse=True)[:3]
    
    cart_count = sum(session.get('cart', {}).values())
    
    html = f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{store['name']}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {{
                --theme-color: {store['theme_color']};
            }}
            .navbar-brand {{ font-weight: bold; font-size: 1.5em; }}
            .product-card {{ 
                transition: all 0.3s ease;
                border: none;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .product-card:hover {{ 
                transform: translateY(-8px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            }}
            .hero-section {{
                background: linear-gradient(135deg, var(--theme-color) 0%, #667eea 100%);
                color: white;
                padding: 80px 0;
            }}
            .category-btn {{
                border: 2px solid var(--theme-color);
                color: var(--theme-color);
                transition: all 0.3s ease;
            }}
            .category-btn:hover, .category-btn.active {{
                background: var(--theme-color);
                color: white;
            }}
            .rating {{ color: #ffc107; }}
            .price {{ font-size: 1.3em; font-weight: bold; color: var(--theme-color); }}
            .btn-primary {{ background: var(--theme-color); border-color: var(--theme-color); }}
            .btn-primary:hover {{ background: var(--theme-color); opacity: 0.9; }}
            .store-info {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
            <div class="container">
                <a class="navbar-brand" href="/{store_slug}" style="color: var(--theme-color);">
                    {store['logo']} {store['name']}
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/{store_slug}">🏠 Trang chủ</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                📋 Danh mục
                            </a>
                            <ul class="dropdown-menu">
    '''
    
    for cat in categories:
        active = 'active' if category_id == cat['id'] else ''
        html += f'''
                                <li><a class="dropdown-item {active}" href="/{store_slug}?category={cat['id']}">{cat['icon']} {cat['name']}</a></li>
        '''
    
    html += f'''
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#about">📞 Liên hệ</a>
                        </li>
                    </ul>
                    
                    <div class="navbar-nav">
                        <a class="nav-link position-relative" href="/{store_slug}/cart">
                            <i class="fas fa-shopping-cart"></i> Giỏ hàng
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                {cart_count}
                            </span>
                        </a>
                        
                        <!-- Store Selector -->
                        <div class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                🏪 Cửa hàng khác
                            </a>
                            <ul class="dropdown-menu">
    '''
    
    for slug, store_info in STORES.items():
        if slug != store_slug:
            html += f'''
                                <li><a class="dropdown-item" href="/{slug}">{store_info['logo']} {store_info['name']}</a></li>
            '''
    
    html += f'''
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero-section">
            <div class="container text-center">
                <h1 class="display-4 fw-bold mb-3">{store['logo']} {store['name']}</h1>
                <p class="lead fs-4">{store['description']}</p>
                <div class="row justify-content-center mt-4">
                    <div class="col-md-8">
                        <div class="store-info text-dark">
                            <div class="row">
                                <div class="col-md-4">
                                    <i class="fas fa-phone text-primary"></i> {store['phone']}
                                </div>
                                <div class="col-md-4">
                                    <i class="fas fa-envelope text-primary"></i> {store['email']}
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

        <!-- Featured Products -->
        <div class="container my-5">
            <h2 class="text-center mb-5">
                <i class="fas fa-star text-warning me-2"></i>Sản phẩm nổi bật
            </h2>
            <div class="row">
    '''
    
    for product in featured_products:
        stars = render_stars(product['rating'])
        html += f'''
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card product-card h-100">
                        <div class="position-relative">
                            <img src="{product['image']}" class="card-img-top" style="height: 250px; object-fit: cover;">
                            <span class="position-absolute top-0 end-0 m-2 badge bg-warning text-dark">
                                ⭐ {product['rating']}
                            </span>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">{product['name']}</h5>
                            <p class="card-text text-muted flex-grow-1">{product['description']}</p>
                            <div class="rating mb-2">{stars} ({product['reviews']} đánh giá)</div>
                            <div class="price mb-3">{product['price']:,}đ</div>
                            <form method="POST" action="/{store_slug}/add-to-cart" class="mt-auto">
                                <input type="hidden" name="product_id" value="{product['id']}">
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="fas fa-cart-plus me-2"></i>Thêm vào giỏ
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
        '''
    
    html += '''
            </div>
        </div>

        <!-- Category Filter -->
        <div class="container">
            <div class="row mb-4">
                <div class="col-12 text-center">
                    <h3 class="mb-4">📋 Danh mục sản phẩm</h3>
                    <div class="btn-group flex-wrap" role="group">
    '''
    
    # Nút "Tất cả"
    active_all = 'active' if not category_id else ''
    html += f'''
                        <a href="/{store_slug}" class="btn category-btn {active_all}">
                            🛍️ Tất cả
                        </a>
    '''
    
    for cat in categories:
        active = 'active' if category_id == cat['id'] else ''
        html += f'''
                        <a href="/{store_slug}?category={cat['id']}" class="btn category-btn {active}">
                            {cat['icon']} {cat['name']}
                        </a>
        '''
    
    html += '''
                    </div>
                </div>
            </div>
        </div>

        <!-- Products Grid -->
        <div class="container mb-5">
            <div class="row">
    '''
    
    for product in products_data['products']:
        stars = render_stars(product['rating'])
        html += f'''
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card product-card h-100">
                        <img src="{product['image']}" class="card-img-top" style="height: 250px; object-fit: cover;">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">{product['name']}</h5>
                            <p class="card-text text-muted flex-grow-1">{product['description']}</p>
                            <div class="rating mb-2">{stars} ({product['reviews']} đánh giá)</div>
                            <div class="price mb-3">{product['price']:,}đ</div>
                            <form method="POST" action="/{store_slug}/add-to-cart" class="mt-auto">
                                <input type="hidden" name="product_id" value="{product['id']}">
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="fas fa-cart-plus me-2"></i>Thêm vào giỏ
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
        '''
    
    html += '''
            </div>
        </div>

        <!-- Pagination -->
    '''
    
    if products_data['pages'] > 1:
        html += f'''
        <div class="container mb-5">
            <nav aria-label="Product pagination">
                <ul class="pagination justify-content-center">
        '''
        
        # Previous button
        if products_data['has_prev']:
            prev_url = f"/{store_slug}?page={products_data['current_page'] - 1}"
            if category_id:
                prev_url += f"&category={category_id}"
            html += f'''
                    <li class="page-item">
                        <a class="page-link" href="{prev_url}">Trước</a>
                    </li>
            '''
        
        # Page numbers
        for page_num in range(1, products_data['pages'] + 1):
            active = 'active' if page_num == products_data['current_page'] else ''
            page_url = f"/{store_slug}?page={page_num}"
            if category_id:
                page_url += f"&category={category_id}"
            html += f'''
                    <li class="page-item {active}">
                        <a class="page-link" href="{page_url}">{page_num}</a>
                    </li>
            '''
        
        # Next button
        if products_data['has_next']:
            next_url = f"/{store_slug}?page={products_data['current_page'] + 1}"
            if category_id:
                next_url += f"&category={category_id}"
            html += f'''
                    <li class="page-item">
                        <a class="page-link" href="{next_url}">Sau</a>
                    </li>
            '''
        
        html += '''
                </ul>
            </nav>
        </div>
        '''
    
    html += f'''
        <!-- About Section -->
        <section id="about" class="bg-light py-5">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6">
                        <h3>{store['logo']} Về {store['name']}</h3>
                        <p class="lead">{store['description']}</p>
                        <p>Chúng tôi cam kết mang đến cho khách hàng những sản phẩm chất lượng nhất với dịch vụ tận tâm.</p>
                    </div>
                    <div class="col-lg-6">
                        <h4>📞 Thông tin liên hệ</h4>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-phone text-primary me-2"></i> {store['phone']}</li>
                            <li><i class="fas fa-envelope text-primary me-2"></i> {store['email']}</li>
                            <li><i class="fas fa-map-marker-alt text-primary me-2"></i> {store['address']}</li>
                        </ul>
                        
                        <h4 class="mt-4">🏪 Cửa hàng khác</h4>
                        <div class="d-flex flex-wrap gap-2">
    '''
    
    for slug, store_info in STORES.items():
        if slug != store_slug:
            html += f'''
                            <a href="/{slug}" class="btn btn-outline-primary btn-sm">
                                {store_info['logo']} {store_info['name']}
                            </a>
            '''
    
    html += f'''
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="bg-dark text-white text-center py-4">
            <div class="container">
                <p>&copy; 2024 {store['name']}. Powered by Flask Multi Store System</p>
                <p>
                    <a href="/demo" class="text-light me-3">🏪 Demo Store</a>
                    <a href="/coffee" class="text-light me-3">☕ Coffee House</a>
                    <a href="/restaurant" class="text-light">🍜 Nhà hàng Việt</a>
                </p>
            </div>
        </footer>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        
        <!-- Smooth scrolling -->
        <script>
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/<store_slug>/cart')
def cart(store_slug):
    store = get_store_data(store_slug)
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    all_products = PRODUCTS.get(store_slug, PRODUCTS['demo'])

    for product_id, quantity in cart.items():
        product = next((p for p in all_products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total

    html = f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Giỏ hàng - {store['name']}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {{ --theme-color: {store['theme_color']}; }}
            .btn-primary {{ background: var(--theme-color); border-color: var(--theme-color); }}
            .text-primary {{ color: var(--theme-color) !important; }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
            <div class="container">
                <a class="navbar-brand fw-bold" href="/{store_slug}" style="color: var(--theme-color);">
                    {store['logo']} {store['name']}
                </a>
                <a class="nav-link" href="/{store_slug}">← Quay lại cửa hàng</a>
            </div>
        </nav>

        <div class="container mt-4">
            <h2 class="mb-4">🛒 Giỏ hàng của bạn</h2>
    '''

    if cart_items:
        html += f'''
            <div class="row">
                <div class="col-lg-8">
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
        '''

        for item in cart_items:
            stars = render_stars(item['product']['rating'])
            html += f'''
                                <tr>
                                    <td>
                                        <strong>{item['product']['name']}</strong><br>
                                        <small class="text-muted">{item['product']['description']}</small><br>
                                        <small class="rating">{stars} ({item['product']['reviews']} đánh giá)</small>
                                    </td>
                                    <td>
                                        <img src="{item['product']['image']}" style="width: 80px; height: 80px; object-fit: cover;" class="rounded">
                                    </td>
                                    <td>
                                        <div class="input-group" style="width: 120px;">
                                            <button class="btn btn-outline-secondary btn-sm" onclick="updateQuantity({item['product']['id']}, -1)">-</button>
                                            <input type="text" class="form-control form-control-sm text-center" value="{item['quantity']}" readonly>
                                            <button class="btn btn-outline-secondary btn-sm" onclick="updateQuantity({item['product']['id']}, 1)">+</button>
                                        </div>
                                    </td>
                                    <td>{item['product']['price']:,}đ</td>
                                    <td class="fw-bold text-primary">{item['total']:,}đ</td>
                                    <td>
                                        <a href="/{store_slug}/remove/{item['product']['id']}" class="btn btn-sm btn-outline-danger"
                                           onclick="return confirm('Xóa sản phẩm này?')">
                                            <i class="fas fa-trash"></i>
                                        </a>
                                    </td>
                                </tr>
            '''

        html += f'''
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">📋 Tóm tắt đơn hàng</h5>
                        </div>
                        <div class="card-body">
                            <div class="d-flex justify-content-between mb-3">
                                <span>Tạm tính:</span>
                                <strong>{total:,}đ</strong>
                            </div>
                            <div class="d-flex justify-content-between mb-3">
                                <span>Phí vận chuyển:</span>
                                <span class="text-success">Miễn phí</span>
                            </div>
                            <hr>
                            <div class="d-flex justify-content-between mb-4">
                                <strong>Tổng cộng:</strong>
                                <strong class="text-primary fs-4">{total:,}đ</strong>
                            </div>

                            <div class="d-grid gap-2">
                                <button class="btn btn-success btn-lg">
                                    <i class="fas fa-credit-card me-2"></i>Thanh toán
                                </button>
                                <a href="/{store_slug}" class="btn btn-outline-secondary">
                                    <i class="fas fa-arrow-left me-2"></i>Tiếp tục mua hàng
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-body">
                            <h6>🎁 Ưu đãi đặc biệt</h6>
                            <ul class="list-unstyled small">
                                <li>✅ Miễn phí vận chuyển</li>
                                <li>✅ Đổi trả trong 7 ngày</li>
                                <li>✅ Hỗ trợ 24/7</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        '''
    else:
        html += f'''
            <div class="text-center py-5">
                <i class="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
                <h3>Giỏ hàng trống</h3>
                <p class="text-muted mb-4">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
                <a href="/{store_slug}" class="btn btn-primary btn-lg">
                    <i class="fas fa-shopping-bag me-2"></i>Bắt đầu mua sắm
                </a>
            </div>
        '''

    html += f'''
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function updateQuantity(productId, change) {{
                fetch('/{store_slug}/update-cart', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        product_id: productId,
                        change: change
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        location.reload();
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/<store_slug>/add-to-cart', methods=['POST'])
def add_to_cart(store_slug):
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    if product_id:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        session['cart'] = cart

    return redirect(url_for('home', store_slug=store_slug))

@app.route('/<store_slug>/remove/<int:product_id>')
def remove_from_cart(store_slug, product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart', store_slug=store_slug))

@app.route('/<store_slug>/update-cart', methods=['POST'])
def update_cart(store_slug):
    data = request.get_json()
    product_id = str(data.get('product_id'))
    change = data.get('change')

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] += change
        if cart[product_id] <= 0:
            del cart[product_id]
        session['cart'] = cart

    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 Flask Multi Store - Advanced Version")
    print("=" * 60)
    print("✅ Menu navigation với dropdown")
    print("✅ Phân trang sản phẩm")
    print("✅ Đánh giá sao và reviews")
    print("✅ Multi-store system")
    print("✅ Responsive design")
    print("✅ Category filtering")
    print("")
    print("🏪 Các cửa hàng có sẵn:")
    for slug, store in STORES.items():
        print(f"   {store['logo']} {store['name']}: http://localhost:5000/{slug}")
    print("")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 60)

    app.run(debug=True, port=5000, host='0.0.0.0')
