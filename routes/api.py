from flask import Blueprint, request, jsonify, session
from models import db
from models.store import Store
from models.product import Product, ProductCategory
from models.order import Order, OrderDetail

api_bp = Blueprint('api', __name__)

def get_current_store():
    """Lấy thông tin cửa hàng hiện tại"""
    store_slug = request.args.get('store', 'demo')
    store = Store.query.filter_by(slug=store_slug, is_active=True).first()
    return store

@api_bp.before_request
def load_store():
    """Load thông tin store cho API"""
    from flask import g
    g.store = get_current_store()
    if not g.store:
        return jsonify({'error': 'Store not found'}), 404

@api_bp.route('/products')
def get_products():
    """API lấy danh sách sản phẩm"""
    from flask import g
    store = g.store
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(store_id=store.id, is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.order_by(Product.sort_order, Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'pagination': {
            'page': products.page,
            'pages': products.pages,
            'per_page': products.per_page,
            'total': products.total,
            'has_next': products.has_next,
            'has_prev': products.has_prev
        }
    })

@api_bp.route('/products/<int:product_id>')
def get_product(product_id):
    """API lấy chi tiết sản phẩm"""
    from flask import g
    store = g.store
    
    product = Product.query.filter_by(
        store_id=store.id,
        id=product_id,
        is_active=True
    ).first()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict())

@api_bp.route('/categories')
def get_categories():
    """API lấy danh sách danh mục"""
    from flask import g
    store = g.store
    
    categories = ProductCategory.query.filter_by(
        store_id=store.id,
        is_active=True
    ).order_by(ProductCategory.sort_order).all()
    
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
        'description': cat.description,
        'image': cat.image,
        'product_count': len(cat.products)
    } for cat in categories])

@api_bp.route('/cart', methods=['GET'])
def get_cart():
    """API lấy giỏ hàng"""
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
                'product': product.to_dict(),
                'quantity': quantity,
                'total': float(item_total)
            })
            total += item_total
    
    return jsonify({
        'items': cart_data,
        'total': float(total),
        'count': sum(cart_items.values())
    })

@api_bp.route('/cart/add', methods=['POST'])
def add_to_cart_api():
    """API thêm sản phẩm vào giỏ hàng"""
    from flask import g
    store = g.store
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id or quantity <= 0:
        return jsonify({'error': 'Invalid product or quantity'}), 400
    
    # Kiểm tra sản phẩm tồn tại
    product = Product.query.filter_by(
        store_id=store.id,
        id=product_id,
        is_active=True
    ).first()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Kiểm tra tồn kho
    if product.manage_stock and product.stock_quantity < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Thêm vào session cart
    cart = session.get('cart', {})
    cart_key = str(product_id)
    
    if cart_key in cart:
        cart[cart_key] += quantity
    else:
        cart[cart_key] = quantity
    
    session['cart'] = cart
    
    return jsonify({
        'message': 'Product added to cart',
        'cart_count': sum(cart.values())
    })

@api_bp.route('/cart/update', methods=['POST'])
def update_cart_api():
    """API cập nhật giỏ hàng"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = data.get('quantity', 0)
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        cart[product_id] = quantity
    elif product_id in cart:
        del cart[product_id]
    
    session['cart'] = cart
    
    return jsonify({
        'message': 'Cart updated',
        'cart_count': sum(cart.values())
    })

@api_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart_api():
    """API xóa sản phẩm khỏi giỏ hàng"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        return jsonify({
            'message': 'Product removed from cart',
            'cart_count': sum(cart.values())
        })
    
    return jsonify({'error': 'Product not in cart'}), 404

@api_bp.route('/store')
def get_store_info():
    """API lấy thông tin cửa hàng"""
    from flask import g
    store = g.store
    
    return jsonify(store.to_dict())
