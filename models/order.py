from datetime import datetime
from . import db

class Order(db.Model):
    """Model cho đơn hàng"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Có thể null cho khách vãng lai
    
    # Mã đơn hàng
    order_number = db.Column(db.String(50), unique=True, nullable=False, comment='Mã đơn hàng')
    
    # Thông tin khách hàng (cho khách vãng lai)
    customer_name = db.Column(db.String(100), comment='Tên khách hàng')
    customer_email = db.Column(db.String(120), comment='Email khách hàng')
    customer_phone = db.Column(db.String(20), comment='SĐT khách hàng')
    customer_address = db.Column(db.Text, comment='Địa chỉ giao hàng')
    
    # Thông tin đơn hàng
    subtotal = db.Column(db.Decimal(10, 2), nullable=False, default=0, comment='Tổng tiền hàng')
    shipping_fee = db.Column(db.Decimal(10, 2), default=0, comment='Phí vận chuyển')
    discount_amount = db.Column(db.Decimal(10, 2), default=0, comment='Số tiền giảm giá')
    total_amount = db.Column(db.Decimal(10, 2), nullable=False, comment='Tổng tiền')
    
    # Trạng thái đơn hàng
    status = db.Column(db.String(20), default='pending', comment='Trạng thái: pending, confirmed, processing, shipped, delivered, cancelled')
    payment_status = db.Column(db.String(20), default='pending', comment='Trạng thái thanh toán: pending, paid, failed, refunded')
    payment_method = db.Column(db.String(50), comment='Phương thức thanh toán')
    
    # Ghi chú
    notes = db.Column(db.Text, comment='Ghi chú đơn hàng')
    admin_notes = db.Column(db.Text, comment='Ghi chú nội bộ')
    
    # Thời gian
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, comment='Thời gian xác nhận')
    shipped_at = db.Column(db.DateTime, comment='Thời gian giao hàng')
    delivered_at = db.Column(db.DateTime, comment='Thời gian hoàn thành')
    
    # Relationships
    order_details = db.relationship('OrderDetail', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    @property
    def status_display(self):
        """Hiển thị trạng thái đơn hàng bằng tiếng Việt"""
        status_map = {
            'pending': 'Chờ xác nhận',
            'confirmed': 'Đã xác nhận',
            'processing': 'Đang xử lý',
            'shipped': 'Đang giao hàng',
            'delivered': 'Đã giao hàng',
            'cancelled': 'Đã hủy'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def payment_status_display(self):
        """Hiển thị trạng thái thanh toán bằng tiếng Việt"""
        status_map = {
            'pending': 'Chờ thanh toán',
            'paid': 'Đã thanh toán',
            'failed': 'Thanh toán thất bại',
            'refunded': 'Đã hoàn tiền'
        }
        return status_map.get(self.payment_status, self.payment_status)
    
    def calculate_total(self):
        """Tính tổng tiền đơn hàng"""
        self.subtotal = sum(detail.total_price for detail in self.order_details)
        self.total_amount = self.subtotal + self.shipping_fee - self.discount_amount
        return self.total_amount

class OrderDetail(db.Model):
    """Model cho chi tiết đơn hàng"""
    __tablename__ = 'order_details'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Thông tin sản phẩm tại thời điểm đặt hàng
    product_name = db.Column(db.String(200), nullable=False, comment='Tên sản phẩm')
    product_price = db.Column(db.Decimal(10, 2), nullable=False, comment='Giá sản phẩm')
    quantity = db.Column(db.Integer, nullable=False, comment='Số lượng')
    total_price = db.Column(db.Decimal(10, 2), nullable=False, comment='Thành tiền')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OrderDetail {self.product_name} x {self.quantity}>'
    
    def calculate_total(self):
        """Tính thành tiền"""
        self.total_price = self.product_price * self.quantity
        return self.total_price
