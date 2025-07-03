# 🚀 HƯỚNG DẪN DEPLOY VÀ CHỈNH SỬA GIAO DIỆN

## 📋 **CHUẨN BỊ DEPLOY**

### **Bước 1: Tạo files cần thiết**

#### **requirements.txt**
```
Flask==2.3.3
gunicorn==21.2.0
```

#### **Procfile** (cho Heroku)
```
web: gunicorn app_with_templates:app
```

#### **runtime.txt** (cho Heroku)
```
python-3.9.20
```

#### **.gitignore**
```
__pycache__/
*.pyc
.env
venv/
.DS_Store
```

## 🌐 **DEPLOY LÊN RAILWAY (MIỄN PHÍ)**

### **Cách 1: Deploy từ GitHub**

1. **Push code lên GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/flask-store.git
git push -u origin main
```

2. **Deploy trên Railway:**
   - Truy cập: https://railway.app
   - Đăng nhập bằng GitHub
   - **New Project** → **Deploy from GitHub repo**
   - Chọn repository của bạn
   - Railway tự động deploy

3. **Cấu hình:**
   - Railway tự detect Flask app
   - Website sẽ có URL: `https://your-app.railway.app`

### **Cách 2: Deploy trực tiếp**

1. **Cài Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Deploy:**
```bash
railway login
railway init
railway up
```

## ☁️ **DEPLOY LÊN HEROKU**

### **Bước 1: Cài Heroku CLI**
- Tải từ: https://devcenter.heroku.com/articles/heroku-cli

### **Bước 2: Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### **Bước 3: Mở website**
```bash
heroku open
```

## 🐳 **DEPLOY BẰNG DOCKER**

### **Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app_with_templates.py"]
```

### **Chạy Docker**
```bash
docker build -t flask-store .
docker run -p 5000:5000 flask-store
```

## 🎨 **CHỈNH SỬA GIAO DIỆN**

### **📁 Cấu trúc files sau khi chạy `app_with_templates.py`:**

```
📁 templates/
  ├── base.html          # Layout chính
  ├── index.html         # Trang chủ
  └── cart.html          # Giỏ hàng

📁 static/
  ├── css/
  │   └── style.css      # CSS tùy chỉnh
  └── js/
      └── main.js        # JavaScript tùy chỉnh
```

### **🎯 Chỉnh sửa màu sắc**

**File: `static/css/style.css`**
```css
:root {
    --theme-color: #e74c3c;        /* Đổi màu chủ đạo */
    --secondary-color: #f39c12;    /* Đổi màu phụ */
}

/* Thêm gradient mới */
.hero-section {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
}
```

### **🖼️ Thay đổi layout**

**File: `templates/index.html`**
```html
<!-- Thêm section mới -->
<section class="my-custom-section py-5 bg-light">
    <div class="container">
        <h2 class="text-center mb-4">Khuyến mãi đặc biệt</h2>
        <div class="row">
            <div class="col-md-6">
                <div class="promo-card">
                    <h4>Giảm 20% cho đơn hàng đầu tiên</h4>
                    <p>Sử dụng mã: FIRST20</p>
                </div>
            </div>
        </div>
    </div>
</section>
```

### **✨ Thêm animations**

**File: `static/css/style.css`**
```css
/* Animation mới */
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.promo-card {
    animation: slideInLeft 0.8s ease;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
```

### **🔧 Thêm JavaScript tương tác**

**File: `static/js/main.js`**
```javascript
// Thêm hiệu ứng click cho buttons
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('click', function(e) {
        // Tạo ripple effect
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// CSS cho ripple effect (thêm vào style.css)
/*
.btn-primary {
    position: relative;
    overflow: hidden;
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}
*/
```

## 🛠️ **CHỈNH SỬA NHANH**

### **Thay đổi thông tin cửa hàng:**
**File: `app_with_templates.py`**
```python
STORES = {
    'demo': {
        'name': 'Tên cửa hàng mới',           # Đổi tên
        'description': 'Mô tả mới',          # Đổi mô tả
        'theme_color': '#e74c3c',            # Đổi màu
        'phone': '0987654321',               # Đổi SĐT
        'email': 'new@email.com',            # Đổi email
    }
}
```

### **Thêm sản phẩm mới:**
```python
PRODUCTS.append({
    'id': 5,
    'name': 'Sản phẩm mới',
    'price': 50000,
    'rating': 4.5,
    'reviews': 100,
    'image': 'URL_hình_ảnh',
    'description': 'Mô tả sản phẩm mới'
})
```

## 📱 **RESPONSIVE DESIGN**

Giao diện đã responsive sẵn với Bootstrap 5:
- ✅ Mobile-first design
- ✅ Tự động adapt trên tablet/mobile
- ✅ Touch-friendly buttons
- ✅ Optimized images

## 🔄 **QUY TRÌNH CHỈNH SỬA**

1. **Chỉnh sửa files** trong `templates/` hoặc `static/`
2. **Save files**
3. **Refresh browser** (F5) để xem thay đổi
4. **Deploy lại** nếu cần update lên server

## 🎯 **TIPS CHỈNH SỬA**

### **Thay đổi nhanh màu sắc:**
- Chỉ cần sửa `--theme-color` trong CSS
- Tất cả elements sẽ tự động đổi màu

### **Thêm trang mới:**
1. Tạo template mới trong `templates/`
2. Thêm route mới trong Python
3. Thêm link navigation

### **Tối ưu hình ảnh:**
- Sử dụng Unsplash: `https://images.unsplash.com/photo-ID?w=400&h=300&fit=crop`
- Hoặc upload lên Cloudinary, Imgur

## 🚀 **KẾT LUẬN**

- **Deploy**: Rất dễ với Railway/Heroku
- **Chỉnh sửa**: Templates riêng biệt, dễ customize
- **Responsive**: Tự động adapt mọi thiết bị
- **Performance**: Optimized với CDN Bootstrap

**Bạn đã sẵn sàng deploy và customize website! 🎉**
