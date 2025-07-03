-- Khởi tạo database với charset UTF8MB4
CREATE DATABASE IF NOT EXISTS multi_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user cho Flask app
CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY 'flask_password';
GRANT ALL PRIVILEGES ON multi_store_db.* TO 'flask_user'@'%';
FLUSH PRIVILEGES;

USE multi_store_db;

-- Thiết lập timezone
SET time_zone = '+07:00';
