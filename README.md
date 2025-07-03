# Multi Store E-commerce System

Hệ thống bán hàng đa cửa hàng được xây dựng bằng Flask, cho phép tạo và quản lý nhiều cửa hàng trực tuyến độc lập.

## 🚀 Tính năng chính

### Frontend (Khách hàng)
- ✅ Trang chủ hiển thị sản phẩm theo cửa hàng
- ✅ Danh mục sản phẩm với phân trang
- ✅ Chi tiết sản phẩm với hình ảnh
- ✅ Giỏ hàng với session storage
- ✅ Thanh toán và đặt hàng
- ✅ Giao diện responsive với Bootstrap 5
- ✅ Theme động theo cấu hình cửa hàng

### Backend (Quản trị)
- ✅ Dashboard với thống kê tổng quan
- ✅ Quản lý danh mục sản phẩm
- ✅ Quản lý sản phẩm (CRUD)
- ✅ Quản lý đơn hàng và cập nhật trạng thái
- ✅ Multi-tenant architecture
- ✅ API RESTful cho tích hợp

### Kiến trúc
- ✅ Flask + SQLAlchemy + MySQL
- ✅ Blueprint pattern cho tổ chức code
- ✅ Model-View-Controller (MVC)
- ✅ Database migrations với Flask-Migrate
- ✅ Docker support cho deployment

## 📋 Yêu cầu hệ thống

- Python 3.8+
- MySQL 5.7+ hoặc 8.0+
- Docker & Docker Compose (tùy chọn)

## 🛠️ Cài đặt

### Cách 1: Cài đặt thủ công

1. **Clone repository**
```bash
git clone <repository-url>
cd Flask
```

2. **Tạo virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

3. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

4. **Cấu hình database**
```bash
# Tạo file .env từ .env.example
cp .env.example .env

# Chỉnh sửa thông tin database trong .env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=multi_store_db
SECRET_KEY=your-secret-key-here
```

5. **Khởi tạo database**
```bash
# Tạo database trong MySQL
mysql -u root -p
CREATE DATABASE multi_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Khởi tạo tables và dữ liệu mẫu
flask init-db-command
```

6. **Chạy ứng dụng**
```bash
python app.py
```

### Cách 2: Sử dụng Docker

1. **Clone repository**
```bash
git clone <repository-url>
cd Flask
```

2. **Chạy với Docker Compose**
```bash
docker-compose up -d
```

3. **Khởi tạo dữ liệu mẫu**
```bash
docker-compose exec web flask init-db-command
```

## 🎯 Sử dụng

### Truy cập ứng dụng

- **Website**: http://localhost:5000?store=demo
- **Admin**: http://localhost:5000/admin?store=demo
- **API**: http://localhost:5000/api

### Tài khoản mặc định

- **Username**: admin
- **Password**: admin123

### Tạo cửa hàng mới

```bash
flask create-store
```

Hoặc sử dụng Docker:
```bash
docker-compose exec web flask create-store
```

## 📁 Cấu trúc dự án

```
Flask/
├── app.py                 # File chính khởi chạy ứng dụng
├── config.py             # Cấu hình ứng dụng
├── requirements.txt      # Dependencies Python
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── models/              # Database models
│   ├── __init__.py
│   ├── store.py         # Model cửa hàng
│   ├── product.py       # Model sản phẩm & danh mục
│   ├── user.py          # Model người dùng
│   └── order.py         # Model đơn hàng
├── routes/              # Route handlers
│   ├── __init__.py
│   ├── main.py          # Routes frontend
│   ├── admin.py         # Routes admin
│   └── api.py           # API endpoints
├── templates/           # HTML templates
│   ├── base.html        # Layout chính
│   ├── main/           # Templates frontend
│   └── admin/          # Templates admin
└── static/             # CSS, JS, images
    └── uploads/        # File uploads
```

## 🗃️ Database Schema

### Bảng chính

1. **stores** - Thông tin cửa hàng
2. **product_categories** - Danh mục sản phẩm
3. **products** - Sản phẩm
4. **users** - Người dùng (admin, khách hàng)
5. **orders** - Đơn hàng
6. **order_details** - Chi tiết đơn hàng

### Quan hệ

- Một Store có nhiều Categories, Products, Orders, Users
- Một Category có nhiều Products
- Một Order có nhiều OrderDetails
- Một Product có nhiều OrderDetails

## 🔧 API Endpoints

### Public API

```
GET  /api/products              # Danh sách sản phẩm
GET  /api/products/{id}         # Chi tiết sản phẩm
GET  /api/categories            # Danh sách danh mục
GET  /api/store                 # Thông tin cửa hàng
```

### Cart API

```
GET  /api/cart                  # Lấy giỏ hàng
POST /api/cart/add              # Thêm vào giỏ hàng
POST /api/cart/update           # Cập nhật giỏ hàng
POST /api/cart/remove           # Xóa khỏi giỏ hàng
```

## 🚀 Deploy lên Railway

1. **Tạo tài khoản Railway**: https://railway.app

2. **Cài đặt Railway CLI**
```bash
npm install -g @railway/cli
```

3. **Login và deploy**
```bash
railway login
railway init
railway add mysql
railway deploy
```

4. **Cấu hình biến môi trường**
```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-production-secret-key
```

## 🔒 Bảo mật

### Trong production cần:

1. **Thay đổi SECRET_KEY**
2. **Sử dụng HTTPS**
3. **Cấu hình CORS đúng cách**
4. **Validation input nghiêm ngặt**
5. **Rate limiting**
6. **Authentication/Authorization**

## 🎨 Tùy chỉnh giao diện

### Thay đổi màu sắc cửa hàng

Trong admin panel, cập nhật:
- `primary_color`: Màu chủ đạo
- `secondary_color`: Màu phụ
- `logo`: Logo cửa hàng
- `banner`: Banner trang chủ

### Custom CSS

Thêm CSS tùy chỉnh trong `static/css/custom.css`

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Hỗ trợ

- Email: support@example.com
- Documentation: [Wiki](link-to-wiki)
- Issues: [GitHub Issues](link-to-issues)

## 🔄 Roadmap

- [ ] Tích hợp thanh toán online (VNPay, MoMo)
- [ ] Hệ thống đánh giá sản phẩm
- [ ] Quản lý kho hàng nâng cao
- [ ] Báo cáo doanh thu chi tiết
- [ ] Mobile app với React Native
- [ ] Tích hợp email marketing
- [ ] Multi-language support
- [ ] SEO optimization tools
