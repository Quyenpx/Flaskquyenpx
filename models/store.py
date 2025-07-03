from datetime import datetime
from . import db

class Store(db.Model):
    """Model cho cửa hàng - cho phép multi-tenant"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='Tên cửa hàng')
    slug = db.Column(db.String(100), unique=True, nullable=False, comment='URL slug cho cửa hàng')
    description = db.Column(db.Text, comment='Mô tả cửa hàng')
    logo = db.Column(db.String(255), comment='Đường dẫn logo')
    banner = db.Column(db.String(255), comment='Đường dẫn banner')
    
    # Thông tin liên hệ
    phone = db.Column(db.String(20), comment='Số điện thoại')
    email = db.Column(db.String(100), comment='Email liên hệ')
    address = db.Column(db.Text, comment='Địa chỉ cửa hàng')
    
    # Cấu hình giao diện
    primary_color = db.Column(db.String(7), default='#007bff', comment='Màu chủ đạo (hex)')
    secondary_color = db.Column(db.String(7), default='#6c757d', comment='Màu phụ (hex)')
    
    # Trạng thái
    is_active = db.Column(db.Boolean, default=True, comment='Cửa hàng có hoạt động không')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('ProductCategory', backref='store', lazy=True, cascade='all, delete-orphan')
    products = db.relationship('Product', backref='store', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='store', lazy=True, cascade='all, delete-orphan')
    users = db.relationship('User', backref='store', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Store {self.name}>'
    
    def to_dict(self):
        """Chuyển đổi object thành dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'logo': self.logo,
            'banner': self.banner,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
