from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    """Model cho người dùng"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    
    # Thông tin cơ bản
    username = db.Column(db.String(80), nullable=False, comment='Tên đăng nhập')
    email = db.Column(db.String(120), nullable=False, comment='Email')
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Thông tin cá nhân
    full_name = db.Column(db.String(100), comment='Họ và tên')
    phone = db.Column(db.String(20), comment='Số điện thoại')
    address = db.Column(db.Text, comment='Địa chỉ')
    
    # Phân quyền
    role = db.Column(db.String(20), default='customer', comment='Vai trò: admin, manager, customer')
    
    # Trạng thái
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    # Unique constraints
    __table_args__ = (
        db.UniqueConstraint('store_id', 'username', name='unique_username_per_store'),
        db.UniqueConstraint('store_id', 'email', name='unique_email_per_store'),
    )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Mã hóa và lưu mật khẩu"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Kiểm tra mật khẩu"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Kiểm tra có phải admin không"""
        return self.role == 'admin'
    
    def is_manager(self):
        """Kiểm tra có phải manager không"""
        return self.role in ['admin', 'manager']
    
    def to_dict(self):
        """Chuyển đổi object thành dictionary (không bao gồm password)"""
        return {
            'id': self.id,
            'store_id': self.store_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
