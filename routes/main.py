from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, g
import json
from datetime import datetime

main_bp = Blueprint('main', __name__)

def get_current_store():
    """Lấy thông tin cửa hàng hiện tại từ subdomain hoặc parameter"""
    from models.store import Store

    store_slug = request.args.get('store')
    if not store_slug:
        # Có thể lấy từ subdomain nếu cần
        store_slug = 'demo'  # Default store

    store = Store.query.filter_by(slug=store_slug, is_active=True).first()
    return store

@main_bp.before_request
def load_store():
    """Load thông tin store cho mọi request"""
    g.store = get_current_store()
    if not g.store:
        return render_template('errors/404.html'), 404

@main_bp.route('/')
def index():
    """Trang chủ hiển thị sản phẩm theo store"""
    from models.product import Product, ProductCategory

    store = g.store

    # Lấy danh mục
    categories = ProductCategory.query.filter_by(
        store_id=store.id,
        is_active=True
    ).order_by(ProductCategory.sort_order).all()

    # Lấy sản phẩm nổi bật
    featured_products = Product.query.filter_by(
        store_id=store.id,
        is_active=True,
        is_featured=True
    ).order_by(Product.sort_order).limit(8).all()

    # Lấy sản phẩm mới nhất
    latest_products = Product.query.filter_by(
        store_id=store.id,
        is_active=True
    ).order_by(Product.created_at.desc()).limit(8).all()

    return render_template('main/index.html',
                         store=store,
                         categories=categories,
                         featured_products=featured_products,
                         latest_products=latest_products)

@main_bp.route('/category/<slug>')
def category(slug):
    """Trang danh mục sản phẩm"""
    from flask import g
    store = g.store
    
    category = ProductCategory.query.filter_by(
        store_id=store.id,
        slug=slug,
        is_active=True
    ).first_or_404()
    
    # Phân trang
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    products = Product.query.filter_by(
        store_id=store.id,
        category_id=category.id,
        is_active=True
    ).order_by(Product.sort_order, Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('main/category.html',
                         store=store,
                         category=category,
                         products=products)

@main_bp.route('/product/<slug>')
def product_detail(slug):
    """Trang chi tiết sản phẩm"""
    from flask import g
    store = g.store
    
    product = Product.query.filter_by(
        store_id=store.id,
        slug=slug,
        is_active=True
    ).first_or_404()
    
    # Sản phẩm liên quan (cùng danh mục)
    related_products = Product.query.filter_by(
        store_id=store.id,
        category_id=product.category_id,
        is_active=True
    ).filter(Product.id != product.id).limit(4).all()
    
    return render_template('main/product_detail.html',
                         store=store,
                         product=product,
                         related_products=related_products)

@main_bp.route('/cart')
def cart():
    """Trang giỏ hàng"""
    from flask import g
    store = g.store
    
    cart_items = session.get('cart', {})
    cart_data = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.filter_by(
            store_id=store.id,
            id=int(product_id),
            is_active=True
        ).first()
        
        if product:
            item_total = product.current_price * quantity
            cart_data.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('main/cart.html',
                         store=store,
                         cart_items=cart_data,
                         cart_total=total)

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Thêm sản phẩm vào giỏ hàng"""
    from flask import g
    store = g.store
    
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id or quantity <= 0:
        flash('Thông tin sản phẩm không hợp lệ', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # Kiểm tra sản phẩm tồn tại
    product = Product.query.filter_by(
        store_id=store.id,
        id=product_id,
        is_active=True
    ).first()
    
    if not product:
        flash('Sản phẩm không tồn tại', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # Kiểm tra tồn kho
    if product.manage_stock and product.stock_quantity < quantity:
        flash('Sản phẩm không đủ số lượng trong kho', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # Thêm vào session cart
    cart = session.get('cart', {})
    cart_key = str(product_id)
    
    if cart_key in cart:
        cart[cart_key] += quantity
    else:
        cart[cart_key] = quantity
    
    session['cart'] = cart
    flash(f'Đã thêm {product.name} vào giỏ hàng', 'success')
    
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/update-cart', methods=['POST'])
def update_cart():
    """Cập nhật giỏ hàng"""
    cart = session.get('cart', {})
    
    for product_id, quantity in request.form.items():
        if product_id.startswith('quantity_'):
            pid = product_id.replace('quantity_', '')
            quantity = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 0
            
            if quantity > 0:
                cart[pid] = quantity
            elif pid in cart:
                del cart[pid]
    
    session['cart'] = cart
    flash('Đã cập nhật giỏ hàng', 'success')
    return redirect(url_for('main.cart'))

@main_bp.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart = session.get('cart', {})
    cart_key = str(product_id)

    if cart_key in cart:
        del cart[cart_key]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng', 'success')

    return redirect(url_for('main.cart'))

@main_bp.route('/checkout')
def checkout():
    """Trang thanh toán"""
    from flask import g
    store = g.store

    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Giỏ hàng trống', 'error')
        return redirect(url_for('main.cart'))

    cart_data = []
    total = 0

    for product_id, quantity in cart_items.items():
        product = Product.query.filter_by(
            store_id=store.id,
            id=int(product_id),
            is_active=True
        ).first()

        if product:
            item_total = product.current_price * quantity
            cart_data.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total

    return render_template('main/checkout.html',
                         store=store,
                         cart_items=cart_data,
                         cart_total=total)

@main_bp.route('/place-order', methods=['POST'])
def place_order():
    """Đặt hàng"""
    from flask import g
    store = g.store

    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Giỏ hàng trống', 'error')
        return redirect(url_for('main.cart'))

    # Lấy thông tin khách hàng
    customer_name = request.form.get('customer_name')
    customer_email = request.form.get('customer_email')
    customer_phone = request.form.get('customer_phone')
    customer_address = request.form.get('customer_address')
    notes = request.form.get('notes', '')

    if not all([customer_name, customer_email, customer_phone, customer_address]):
        flash('Vui lòng điền đầy đủ thông tin', 'error')
        return redirect(url_for('main.checkout'))

    try:
        # Tạo đơn hàng
        order = Order(
            store_id=store.id,
            order_number=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            notes=notes,
            status='pending',
            payment_status='pending'
        )

        db.session.add(order)
        db.session.flush()  # Để lấy order.id

        # Tạo chi tiết đơn hàng
        subtotal = 0
        for product_id, quantity in cart_items.items():
            product = Product.query.filter_by(
                store_id=store.id,
                id=int(product_id),
                is_active=True
            ).first()

            if product:
                # Kiểm tra tồn kho
                if product.manage_stock and product.stock_quantity < quantity:
                    flash(f'Sản phẩm {product.name} không đủ số lượng trong kho', 'error')
                    db.session.rollback()
                    return redirect(url_for('main.checkout'))

                order_detail = OrderDetail(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    product_price=product.current_price,
                    quantity=quantity
                )
                order_detail.calculate_total()
                subtotal += order_detail.total_price

                db.session.add(order_detail)

                # Trừ tồn kho
                if product.manage_stock:
                    product.stock_quantity -= quantity

        # Cập nhật tổng tiền đơn hàng
        order.subtotal = subtotal
        order.total_amount = subtotal  # Có thể thêm phí ship sau

        db.session.commit()

        # Xóa giỏ hàng
        session.pop('cart', None)

        flash('Đặt hàng thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.', 'success')
        return redirect(url_for('main.order_success', order_id=order.id))

    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại.', 'error')
        return redirect(url_for('main.checkout'))

@main_bp.route('/order-success/<int:order_id>')
def order_success(order_id):
    """Trang thành công sau khi đặt hàng"""
    from flask import g
    store = g.store

    order = Order.query.filter_by(
        store_id=store.id,
        id=order_id
    ).first_or_404()

    return render_template('main/order_success.html',
                         store=store,
                         order=order)
