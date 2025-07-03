#!/usr/bin/env python3
"""
Flask Multi Store - Phiên bản cực đơn giản
Chỉ cần Flask, không cần gì khác
"""

from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'demo-key-123'

# Dữ liệu sản phẩm
products = [
    {'id': 1, 'name': 'Bánh mì', 'price': 25000, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop'},
    {'id': 2, 'name': 'Phở bò', 'price': 45000, 'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=300&h=200&fit=crop'},
    {'id': 3, 'name': 'Cơm tấm', 'price': 35000, 'image': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=300&h=200&fit=crop'},
    {'id': 4, 'name': 'Cà phê', 'price': 20000, 'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300&h=200&fit=crop'},
]

@app.route('/')
def home():
    cart_count = sum(session.get('cart', {}).values())
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cửa hàng Demo</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .product-card {{ transition: transform 0.2s; }}
            .product-card:hover {{ transform: translateY(-5px); }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand fw-bold" href="/">🏪 Cửa hàng Demo</a>
                <a class="nav-link" href="/cart">
                    🛒 Giỏ hàng <span class="badge bg-danger">{cart_count}</span>
                </a>
            </div>
        </nav>
        
        <div class="container mt-4">
            <div class="jumbotron bg-primary text-white text-center p-5 rounded mb-4">
                <h1>Chào mừng đến cửa hàng!</h1>
                <p>Đồ ăn và đồ uống ngon, giá rẻ</p>
            </div>
            
            <h2>Sản phẩm của chúng tôi</h2>
            <div class="row">
    '''
    
    for product in products:
        html += f'''
                <div class="col-md-6 col-lg-3 mb-4">
                    <div class="card product-card h-100">
                        <img src="{product['image']}" class="card-img-top" style="height: 200px; object-fit: cover;">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">{product['name']}</h5>
                            <p class="text-primary fw-bold">{product['price']:,}đ</p>
                            <form method="POST" action="/add-to-cart" class="mt-auto">
                                <input type="hidden" name="product_id" value="{product['id']}">
                                <button type="submit" class="btn btn-primary w-100">
                                    Thêm vào giỏ
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
        '''
    
    html += '''
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
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
    <html>
    <head>
        <title>Giỏ hàng - Cửa hàng Demo</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand fw-bold" href="/">🏪 Cửa hàng Demo</a>
                <a class="nav-link" href="/cart">
                    🛒 Giỏ hàng <span class="badge bg-danger">{len(cart_items)}</span>
                </a>
            </div>
        </nav>
        
        <div class="container mt-4">
            <h2>🛒 Giỏ hàng của bạn</h2>
    '''
    
    if cart_items:
        html += '''
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
                            <td><strong>{item['product']['name']}</strong></td>
                            <td><img src="{item['product']['image']}" style="width: 50px; height: 50px; object-fit: cover;" class="rounded"></td>
                            <td>{item['quantity']}</td>
                            <td>{item['product']['price']:,}đ</td>
                            <td class="fw-bold text-primary">{item['total']:,}đ</td>
                            <td>
                                <a href="/remove/{item['product']['id']}" class="btn btn-sm btn-outline-danger"
                                   onclick="return confirm('Xóa sản phẩm này?')">🗑️</a>
                            </td>
                        </tr>
            '''
        
        html += f'''
                    </tbody>
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
                    <a href="/" class="btn btn-outline-secondary btn-lg">
                        ← Tiếp tục mua hàng
                    </a>
                </div>
                <div class="col-md-6 text-end">
                    <button class="btn btn-success btn-lg">
                        💳 Thanh toán ({total:,}đ)
                    </button>
                </div>
            </div>
        '''
    else:
        html += '''
            <div class="text-center py-5">
                <h3>🛒 Giỏ hàng trống</h3>
                <p class="text-muted">Bạn chưa có sản phẩm nào trong giỏ hàng</p>
                <a href="/" class="btn btn-primary btn-lg">🛍️ Bắt đầu mua sắm</a>
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
    print("🚀 Flask Multi Store - Super Simple Version")
    print("=" * 50)
    print("✅ Chỉ cần Flask - không cần gì khác")
    print("✅ HTML inline - không cần template files")
    print("✅ Dữ liệu trong memory - không cần database")
    print("✅ Ảnh từ Unsplash")
    print("🌐 Trang chủ: http://localhost:5000")
    print("🛒 Giỏ hàng: http://localhost:5000/cart")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
