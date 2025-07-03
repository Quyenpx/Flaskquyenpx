# 🚀 Hướng dẫn chạy nhanh Flask Multi Store

## Cách 1: Chạy nhanh nhất (Khuyến nghị)

### Bước 1: Cài đặt Flask
```bash
pip install flask flask-sqlalchemy
```

### Bước 2: Chạy ứng dụng
```bash
python quick_start.py
```

### Bước 3: Thiết lập
1. Mở trình duyệt: http://localhost:5000/create-templates
2. Sau đó: http://localhost:5000/setup
3. Cuối cùng: http://localhost:5000?store=demo

## Cách 2: Chạy đầy đủ

### Bước 1: Cài đặt dependencies
```bash
pip install -r requirements_local.txt
```

### Bước 2: Chạy script setup
```bash
python setup_and_run.py
```

### Bước 3: Hoặc chạy trực tiếp
```bash
python run_local.py
```

## Cách 3: Nếu gặp lỗi

### Kiểm tra Python version
```bash
python --version
# Cần Python 3.8+
```

### Cài đặt từng package
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-wtf
pip install werkzeug
```

### Chạy từng bước
```bash
# 1. Tạo virtual environment (tùy chọn)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# 2. Cài đặt Flask
pip install flask flask-sqlalchemy

# 3. Chạy quick start
python quick_start.py
```

## 🎯 Truy cập ứng dụng

- **Website**: http://localhost:5000?store=demo
- **Giỏ hàng**: http://localhost:5000/cart?store=demo

## 🔧 Tính năng có sẵn

✅ Hiển thị sản phẩm  
✅ Thêm vào giỏ hàng  
✅ Xem giỏ hàng  
✅ Giao diện responsive  
✅ Multi-store support  

## ❌ Khắc phục lỗi thường gặp

### Lỗi: ModuleNotFoundError
```bash
pip install flask flask-sqlalchemy
```

### Lỗi: Port đã được sử dụng
- Thay đổi port trong file: `app.run(port=5001)`
- Hoặc tắt ứng dụng khác đang dùng port 5000

### Lỗi: Template not found
```bash
# Chạy để tạo templates
python quick_start.py
# Truy cập: http://localhost:5000/create-templates
```

### Lỗi: Database
- Xóa file `quick_store.db` và chạy lại
- Hoặc truy cập: http://localhost:5000/setup

## 📞 Hỗ trợ

Nếu vẫn gặp lỗi, hãy:
1. Kiểm tra Python version >= 3.8
2. Cài đặt lại Flask: `pip install --upgrade flask`
3. Chạy: `python quick_start.py`
4. Báo lỗi cụ thể để được hỗ trợ

## 🎉 Thành công!

Khi thấy:
```
🚀 Quick Start Flask Multi Store
📝 Truy cập: http://localhost:5000/create-templates
* Running on http://127.0.0.1:5000
```

Có nghĩa là đã chạy thành công! 🎊
