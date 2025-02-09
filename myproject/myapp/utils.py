import hashlib
import os
from django.shortcuts import redirect


def hash_password_with_salt(password):
    """
    Tạo hash từ mật khẩu và salt ngẫu nhiên.
    """
    # Tạo salt ngẫu nhiên (16 byte)
    salt = os.urandom(16)
    # Kết hợp mật khẩu và salt để hash
    hashed = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    # Lưu salt và hash trong cùng một chuỗi
    return salt.hex() + ":" + hashed

def check_password_with_salt(password, stored_password):
    """
    Kiểm tra mật khẩu người dùng nhập với mật khẩu đã lưu (salt + hash).
    """
    # Tách salt và hash từ stored_password
    salt, hashed = stored_password.split(':')
    # Hash lại mật khẩu nhập vào với salt
    return hashlib.sha256(bytes.fromhex(salt) + password.encode('utf-8')).hexdigest() == hashed

def login_required_custom(view_func):
    """
    Decorator để kiểm tra xem người dùng đã đăng nhập chưa.
    Nếu chưa, chuyển hướng đến trang đăng nhập.
    """
    def wrapper(request, *args, **kwargs):
        if 'userid' not in request.session:
            # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
            return redirect('/manager/admin-login/')
        return view_func(request, *args, **kwargs)
    return wrapper