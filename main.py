#!/usr/bin/env python3
"""
Flask Multi Store - Deploy version for Railway
"""

import os
from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'railway-deploy-key-2024')

# Dữ liệu sản phẩm
products = [
    {'id': 1, 'name': 'Bánh mì thịt nướng', 'price': 25000, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop'},
    {'id': 2, 'name': 'Phở bò đặc biệt', 'price': 45000, 'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop'},
    {'id': 3, 'name': 'Cơm tấm sườn nướng', 'price': 35000, 'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop'},
    {'id': 4, 'name': 'Cà phê sữa đá', 'price': 20000, 'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop'},
    {'id': 5, 'name': 'Trà sữa trân châu', 'price': 30000, 'image': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop'},
    {'id': 6, 'name': 'Nước ép cam tươi', 'price': 25000, 'image': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop'},
]

@app.route('/')
def home():
    cart_count = sum(session.get('cart', {}).values())
    
    html = f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏪 Cửa hàng Online</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .product-card {{ 
                transition: all 0.3s ease;
                border: none;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-radius: 15px;
                overflow: hidden;
            }}
            .product-card:hover {{ 
                transform: translateY(-8px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            }}
            .hero {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 80px 0;
            }}
            .product-image {{
                height: 200px;
                object-fit: cover;
                transition: transform 0.3s ease;
            }}
            .product-card:hover .product-image {{
                transform: scale(1.05);
            }}
            .btn-primary {{
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            .navbar-brand {{
                font-size: 1.5em;
                font-weight: bold;
            }}
            .price {{
                font-size: 1.3em;
                font-weight: bold;
                color: #e74c3c;
            }}
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
            <div class="container">
                <a class="navbar-brand text-primary" href="/">
                    <i class="fas fa-store me-2"></i>Cửa hàng Online
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link position-relative" href="/cart">
                        <i class="fas fa-shopping-cart"></i> Giỏ hàng
                        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                            {cart_count}
                        </span>
                    </a>
                </div>
            </div>
        </nav>
        
        <!-- Hero Section -->
        <section class="hero text-white">
            <div class="container text-center">
                <h1 class="display-4 fw-bold mb-3">
                    <i class="fas fa-store me-3"></i>Cửa hàng Online
                </h1>
                <p class="lead fs-4">Đồ ăn và đồ uống ngon, giao hàng tận nơi</p>
                <div class="row justify-content-center mt-4">
                    <div class="col-md-8">
                        <div class="bg-white bg-opacity-10 p-4 rounded">
                            <div class="row text-center">
                                <div class="col-md-4">
                                    <i class="fas fa-shipping-fast fa-2x mb-2"></i>
                                    <p>Giao hàng nhanh</p>
                                </div>
                                <div class="col-md-4">
                                    <i class="fas fa-shield-alt fa-2x mb-2"></i>
                                    <p>Chất lượng đảm bảo</p>
                                </div>
                                <div class="col-md-4">
                                    <i class="fas fa-headset fa-2x mb-2"></i>
                                    <p>Hỗ trợ 24/7</p>
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
                <i class="fas fa-utensils text-primary me-2"></i>Sản phẩm nổi bật
            </h2>
            <div class="row">
    '''
    
    for product in products:
        html += f'''
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card product-card h-100">
                        <img src="{product['image']}" class="card-img-top product-image" alt="{product['name']}">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">{product['name']}</h5>
                            <div class="price mb-3">{product['price']:,}đ</div>
                            <form method="POST" action="/add-to-cart" class="mt-auto">
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
        
        <!-- Call to Action -->
        <section class="bg-light py-5">
            <div class="container text-center">
                <h3 class="mb-4">Đặt hàng ngay hôm nay!</h3>
                <p class="lead text-muted mb-4">Giao hàng miễn phí cho đơn hàng từ 100,000đ</p>
                <a href="#products" class="btn btn-primary btn-lg">
                    <i class="fas fa-shopping-bag me-2"></i>Mua ngay
                </a>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="bg-dark text-white text-center py-4">
            <div class="container">
                <p class="mb-2">&copy; 2024 Cửa hàng Online. Powered by Flask & Railway</p>
                <p class="mb-0">
                    <i class="fas fa-phone me-2"></i>0123456789 |
                    <i class="fas fa-envelope me-2"></i>contact@store.com
                </p>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        
        <!-- Smooth scrolling -->
        <script>
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{ behavior: 'smooth' }});
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
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
        <title>🛒 Giỏ hàng - Cửa hàng Online</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-light bg-light shadow-sm">
            <div class="container">
                <a class="navbar-brand fw-bold text-primary" href="/">
                    <i class="fas fa-store me-2"></i>Cửa hàng Online
                </a>
                <a class="nav-link" href="/">
                    <i class="fas fa-arrow-left me-1"></i>Quay lại
                </a>
            </div>
        </nav>
        
        <div class="container mt-4">
            <h2 class="mb-4">
                <i class="fas fa-shopping-cart me-2"></i>Giỏ hàng của bạn
            </h2>
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
            html += f'''
                                <tr>
                                    <td>
                                        <strong>{item['product']['name']}</strong>
                                    </td>
                                    <td>
                                        <img src="{item['product']['image']}" style="width: 60px; height: 60px; object-fit: cover;" class="rounded">
                                    </td>
                                    <td>
                                        <span class="badge bg-primary fs-6">{item['quantity']}</span>
                                    </td>
                                    <td>{item['product']['price']:,}đ</td>
                                    <td class="fw-bold text-primary">{item['total']:,}đ</td>
                                    <td>
                                        <a href="/remove/{item['product']['id']}" class="btn btn-sm btn-outline-danger"
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
                            <h5 class="mb-0">
                                <i class="fas fa-receipt me-2"></i>Tóm tắt đơn hàng
                            </h5>
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
                                <a href="/" class="btn btn-outline-secondary">
                                    <i class="fas fa-arrow-left me-2"></i>Tiếp tục mua hàng
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        '''
    else:
        html += '''
            <div class="text-center py-5">
                <i class="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
                <h3>Giỏ hàng trống</h3>
                <p class="text-muted mb-4">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
                <a href="/" class="btn btn-primary btn-lg">
                    <i class="fas fa-shopping-bag me-2"></i>Bắt đầu mua sắm
                </a>
            </div>
        '''
    
    html += '''
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
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

if __name__ == '__main__':
    # Cấu hình cho Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
