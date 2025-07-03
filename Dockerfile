# Sử dụng Python 3.9 image (không phải slim để tránh lỗi)
FROM python:3.9

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt Python dependencies
COPY requirements_deploy.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Tạo thư mục static nếu chưa có
RUN mkdir -p static/css static/js templates

# Thiết lập biến môi trường
ENV FLASK_APP=app_with_templates.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app_with_templates.py"]
