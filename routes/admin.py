from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db
from models.store import Store
from models.product import Product, ProductCategory
from models.order import Order, OrderDetail
from models.user import User
from werkzeug.utils import secure_filename
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def get_current_store():
    """Lấy thông tin cửa hàng hiện tại"""
    store_slug = request.args.get('store', 'demo')
    store = Store.query.filter_by(slug=store_slug, is_active=True).first()
    return store

def admin_required(f):
    """Decorator kiểm tra quyền admin"""
    def decorated_function(*args, **kwargs):
        # Tạm thời bỏ qua authentication cho demo
        # Trong thực tế cần kiểm tra session/login
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.before_request
def load_store():
    """Load thông tin store cho admin"""
    from flask import g
    g.store = get_current_store()
    if not g.store:
        return render_template('errors/store_not_found.html'), 404

@admin_bp.route('/')
@admin_required
def dashboard():
    """Trang dashboard admin"""
    from flask import g
    store = g.store
    
    # Thống kê cơ bản
    total_products = Product.query.filter_by(store_id=store.id).count()
    total_orders = Order.query.filter_by(store_id=store.id).count()
    pending_orders = Order.query.filter_by(store_id=store.id, status='pending').count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(
        store_id=store.id, payment_status='paid'
    ).scalar() or 0
    
    # Đơn hàng gần đây
    recent_orders = Order.query.filter_by(store_id=store.id).order_by(
        Order.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         store=store,
                         total_products=total_products,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

# QUẢN LÝ DANH MỤC
@admin_bp.route('/categories')
@admin_required
def categories():
    """Danh sách danh mục"""
    from flask import g
    store = g.store
    
    categories = ProductCategory.query.filter_by(store_id=store.id).order_by(
        ProductCategory.sort_order
    ).all()
    
    return render_template('admin/categories.html',
                         store=store,
                         categories=categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    """Thêm danh mục"""
    from flask import g
    store = g.store
    
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description', '')
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = 'is_active' in request.form
        
        if not name or not slug:
            flash('Tên và slug là bắt buộc', 'error')
            return render_template('admin/category_form.html', store=store)
        
        # Kiểm tra slug trùng
        existing = ProductCategory.query.filter_by(
            store_id=store.id, slug=slug
        ).first()
        if existing:
            flash('Slug đã tồn tại', 'error')
            return render_template('admin/category_form.html', store=store)
        
        category = ProductCategory(
            store_id=store.id,
            name=name,
            slug=slug,
            description=description,
            sort_order=sort_order,
            is_active=is_active
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Thêm danh mục thành công', 'success')
        return redirect(url_for('admin.categories', store=store.slug))
    
    return render_template('admin/category_form.html', store=store)

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_category(id):
    """Sửa danh mục"""
    from flask import g
    store = g.store
    
    category = ProductCategory.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = request.form.get('slug')
        category.description = request.form.get('description', '')
        category.sort_order = request.form.get('sort_order', 0, type=int)
        category.is_active = 'is_active' in request.form
        
        if not category.name or not category.slug:
            flash('Tên và slug là bắt buộc', 'error')
            return render_template('admin/category_form.html', 
                                 store=store, category=category)
        
        # Kiểm tra slug trùng (trừ chính nó)
        existing = ProductCategory.query.filter_by(
            store_id=store.id, slug=category.slug
        ).filter(ProductCategory.id != id).first()
        if existing:
            flash('Slug đã tồn tại', 'error')
            return render_template('admin/category_form.html', 
                                 store=store, category=category)
        
        db.session.commit()
        flash('Cập nhật danh mục thành công', 'success')
        return redirect(url_for('admin.categories', store=store.slug))
    
    return render_template('admin/category_form.html', 
                         store=store, category=category)

@admin_bp.route('/categories/delete/<int:id>')
@admin_required
def delete_category(id):
    """Xóa danh mục"""
    from flask import g
    store = g.store
    
    category = ProductCategory.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()
    
    # Kiểm tra có sản phẩm không
    if category.products:
        flash('Không thể xóa danh mục có sản phẩm', 'error')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Xóa danh mục thành công', 'success')
    
    return redirect(url_for('admin.categories', store=store.slug))

# QUẢN LÝ SẢN PHẨM
@admin_bp.route('/products')
@admin_required
def products():
    """Danh sách sản phẩm"""
    from flask import g
    store = g.store
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    products = Product.query.filter_by(store_id=store.id).order_by(
        Product.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/products.html',
                         store=store,
                         products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Thêm sản phẩm"""
    from flask import g
    store = g.store
    
    categories = ProductCategory.query.filter_by(
        store_id=store.id, is_active=True
    ).order_by(ProductCategory.sort_order).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        category_id = request.form.get('category_id', type=int)
        description = request.form.get('description', '')
        short_description = request.form.get('short_description', '')
        price = request.form.get('price', type=float)
        sale_price = request.form.get('sale_price', type=float) or None
        stock_quantity = request.form.get('stock_quantity', 0, type=int)
        manage_stock = 'manage_stock' in request.form
        is_active = 'is_active' in request.form
        is_featured = 'is_featured' in request.form
        sort_order = request.form.get('sort_order', 0, type=int)
        
        if not all([name, slug, category_id, price]):
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
            return render_template('admin/product_form.html', 
                                 store=store, categories=categories)
        
        # Kiểm tra slug trùng
        existing = Product.query.filter_by(
            store_id=store.id, slug=slug
        ).first()
        if existing:
            flash('Slug đã tồn tại', 'error')
            return render_template('admin/product_form.html', 
                                 store=store, categories=categories)
        
        product = Product(
            store_id=store.id,
            category_id=category_id,
            name=name,
            slug=slug,
            description=description,
            short_description=short_description,
            price=price,
            sale_price=sale_price,
            stock_quantity=stock_quantity,
            manage_stock=manage_stock,
            is_active=is_active,
            is_featured=is_featured,
            sort_order=sort_order
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Thêm sản phẩm thành công', 'success')
        return redirect(url_for('admin.products', store=store.slug))
    
    return render_template('admin/product_form.html',
                         store=store, categories=categories)

# QUẢN LÝ ĐỚN HÀNG
@admin_bp.route('/orders')
@admin_required
def orders():
    """Danh sách đơn hàng"""
    from flask import g
    store = g.store

    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    per_page = 20

    query = Order.query.filter_by(store_id=store.id)

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('admin/orders.html',
                         store=store,
                         orders=orders,
                         current_status=status)

@admin_bp.route('/orders/<int:id>')
@admin_required
def order_detail(id):
    """Chi tiết đơn hàng"""
    from flask import g
    store = g.store

    order = Order.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    return render_template('admin/order_detail.html',
                         store=store,
                         order=order)

@admin_bp.route('/orders/<int:id>/update-status', methods=['POST'])
@admin_required
def update_order_status(id):
    """Cập nhật trạng thái đơn hàng"""
    from flask import g
    store = g.store

    order = Order.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes', '')

    if new_status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        if admin_notes:
            order.admin_notes = admin_notes

        # Cập nhật thời gian tương ứng
        if new_status == 'confirmed':
            order.confirmed_at = datetime.utcnow()
        elif new_status == 'shipped':
            order.shipped_at = datetime.utcnow()
        elif new_status == 'delivered':
            order.delivered_at = datetime.utcnow()

        db.session.commit()
        flash('Cập nhật trạng thái đơn hàng thành công', 'success')
    else:
        flash('Trạng thái không hợp lệ', 'error')

    return redirect(url_for('admin.order_detail', id=id, store=store.slug))

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    """Sửa sản phẩm"""
    from flask import g
    store = g.store

    product = Product.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    categories = ProductCategory.query.filter_by(
        store_id=store.id, is_active=True
    ).order_by(ProductCategory.sort_order).all()

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.slug = request.form.get('slug')
        product.category_id = request.form.get('category_id', type=int)
        product.description = request.form.get('description', '')
        product.short_description = request.form.get('short_description', '')
        product.price = request.form.get('price', type=float)
        product.sale_price = request.form.get('sale_price', type=float) or None
        product.stock_quantity = request.form.get('stock_quantity', 0, type=int)
        product.manage_stock = 'manage_stock' in request.form
        product.is_active = 'is_active' in request.form
        product.is_featured = 'is_featured' in request.form
        product.sort_order = request.form.get('sort_order', 0, type=int)

        if not all([product.name, product.slug, product.category_id, product.price]):
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
            return render_template('admin/product_form.html',
                                 store=store, categories=categories, product=product)

        # Kiểm tra slug trùng (trừ chính nó)
        existing = Product.query.filter_by(
            store_id=store.id, slug=product.slug
        ).filter(Product.id != id).first()
        if existing:
            flash('Slug đã tồn tại', 'error')
            return render_template('admin/product_form.html',
                                 store=store, categories=categories, product=product)

        db.session.commit()
        flash('Cập nhật sản phẩm thành công', 'success')
        return redirect(url_for('admin.products', store=store.slug))

    return render_template('admin/product_form.html',
                         store=store, categories=categories, product=product)

@admin_bp.route('/products/delete/<int:id>')
@admin_required
def delete_product(id):
    """Xóa sản phẩm"""
    from flask import g
    store = g.store

    product = Product.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    # Kiểm tra có trong đơn hàng không
    if product.order_details:
        flash('Không thể xóa sản phẩm đã có trong đơn hàng', 'error')
    else:
        db.session.delete(product)
        db.session.commit()
        flash('Xóa sản phẩm thành công', 'success')

    return redirect(url_for('admin.products', store=store.slug))

# QUẢN LÝ ĐỚN HÀNG
@admin_bp.route('/orders')
@admin_required
def orders():
    """Danh sách đơn hàng"""
    from flask import g
    store = g.store

    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    per_page = 20

    query = Order.query.filter_by(store_id=store.id)

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('admin/orders.html',
                         store=store,
                         orders=orders,
                         current_status=status)

@admin_bp.route('/orders/<int:id>')
@admin_required
def order_detail(id):
    """Chi tiết đơn hàng"""
    from flask import g
    store = g.store

    order = Order.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    return render_template('admin/order_detail.html',
                         store=store,
                         order=order)

@admin_bp.route('/orders/<int:id>/update-status', methods=['POST'])
@admin_required
def update_order_status(id):
    """Cập nhật trạng thái đơn hàng"""
    from flask import g
    store = g.store

    order = Order.query.filter_by(
        store_id=store.id, id=id
    ).first_or_404()

    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes', '')

    if new_status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        if admin_notes:
            order.admin_notes = admin_notes

        # Cập nhật thời gian tương ứng
        if new_status == 'confirmed':
            order.confirmed_at = datetime.utcnow()
        elif new_status == 'shipped':
            order.shipped_at = datetime.utcnow()
        elif new_status == 'delivered':
            order.delivered_at = datetime.utcnow()

        db.session.commit()
        flash('Cập nhật trạng thái đơn hàng thành công', 'success')
    else:
        flash('Trạng thái không hợp lệ', 'error')

    return redirect(url_for('admin.order_detail', id=id, store=store.slug))
