from datetime import datetime
from . import db

class ProductCategory(db.Model):
    """Model cho danh mục sản phẩm"""
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, comment='Tên danh mục')
    slug = db.Column(db.String(100), nullable=False, comment='URL slug')
    description = db.Column(db.Text, comment='Mô tả danh mục')
    image = db.Column(db.String(255), comment='Hình ảnh danh mục')
    sort_order = db.Column(db.Integer, default=0, comment='Thứ tự sắp xếp')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    # Unique constraint cho slug trong cùng store
    __table_args__ = (db.UniqueConstraint('store_id', 'slug', name='unique_category_slug_per_store'),)
    
    def __repr__(self):
        return f'<ProductCategory {self.name}>'

class Product(db.Model):
    """Model cho sản phẩm"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False, comment='Tên sản phẩm')
    slug = db.Column(db.String(200), nullable=False, comment='URL slug')
    description = db.Column(db.Text, comment='Mô tả sản phẩm')
    short_description = db.Column(db.String(500), comment='Mô tả ngắn')
    
    # Giá cả
    price = db.Column(db.Decimal(10, 2), nullable=False, comment='Giá bán')
    sale_price = db.Column(db.Decimal(10, 2), comment='Giá khuyến mãi')
    cost_price = db.Column(db.Decimal(10, 2), comment='Giá vốn')
    
    # Hình ảnh
    image = db.Column(db.String(255), comment='Hình ảnh chính')
    gallery = db.Column(db.Text, comment='Gallery hình ảnh (JSON)')
    
    # Kho hàng
    stock_quantity = db.Column(db.Integer, default=0, comment='Số lượng tồn kho')
    manage_stock = db.Column(db.Boolean, default=True, comment='Quản lý tồn kho')
    
    # SEO
    meta_title = db.Column(db.String(200), comment='Meta title')
    meta_description = db.Column(db.String(500), comment='Meta description')
    
    # Trạng thái
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False, comment='Sản phẩm nổi bật')
    sort_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_details = db.relationship('OrderDetail', backref='product', lazy=True)
    
    # Unique constraint cho slug trong cùng store
    __table_args__ = (db.UniqueConstraint('store_id', 'slug', name='unique_product_slug_per_store'),)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def current_price(self):
        """Trả về giá hiện tại (sale_price nếu có, không thì price)"""
        return self.sale_price if self.sale_price else self.price
    
    @property
    def is_on_sale(self):
        """Kiểm tra sản phẩm có đang giảm giá không"""
        return self.sale_price is not None and self.sale_price < self.price
    
    @property
    def discount_percentage(self):
        """Tính phần trăm giảm giá"""
        if self.is_on_sale:
            return round(((self.price - self.sale_price) / self.price) * 100)
        return 0
    
    def to_dict(self):
        """Chuyển đổi object thành dictionary"""
        return {
            'id': self.id,
            'store_id': self.store_id,
            'category_id': self.category_id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'short_description': self.short_description,
            'price': float(self.price),
            'sale_price': float(self.sale_price) if self.sale_price else None,
            'current_price': float(self.current_price),
            'image': self.image,
            'stock_quantity': self.stock_quantity,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'is_on_sale': self.is_on_sale,
            'discount_percentage': self.discount_percentage
        }
