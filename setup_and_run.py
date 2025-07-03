#!/usr/bin/env python3
"""
Script setup và chạy ứng dụng Flask Multi Store
Sử dụng SQLite để dễ dàng chạy local mà không cần MySQL
"""

import os
import sys
import subprocess

def install_requirements():
    """Cài đặt requirements"""
    print("📦 Đang cài đặt dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt dependencies thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt dependencies: {e}")
        return False

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def main():
    """Hàm chính"""
    print("🚀 Flask Multi Store - Setup & Run")
    print("=" * 50)
    
    # Kiểm tra Python version
    if not check_python_version():
        return
    
    # Kiểm tra requirements.txt
    if not os.path.exists('requirements.txt'):
        print("❌ Không tìm thấy requirements.txt")
        return
    
    # Cài đặt dependencies
    if not install_requirements():
        return
    
    print("\n🔧 Đang khởi động ứng dụng...")
    
    # Import và chạy app
    try:
        from run_local import main as run_app
        run_app()
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("Đang thử chạy trực tiếp...")
        
        # Fallback: chạy trực tiếp
        try:
            import run_local
            run_local.main()
        except Exception as e:
            print(f"❌ Lỗi khi chạy ứng dụng: {e}")
            print("\n🔍 Hướng dẫn khắc phục:")
            print("1. Kiểm tra đã cài đặt đúng dependencies")
            print("2. Chạy: python run_local.py")
            print("3. Hoặc liên hệ hỗ trợ")

if __name__ == '__main__':
    main()
