import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Định nghĩa BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Đọc SECRET_KEY từ .env (nếu thiếu, dùng giá trị mặc định)
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")

# Đọc DEBUG từ .env (chuyển sang kiểu Boolean)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Đọc ALLOWED_HOSTS từ .env (nếu thiếu, mặc định là localhost)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# **QUAN TRỌNG: Cần có INSTALLED_APPS đầy đủ**
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Thêm django_apscheduler vào đây
    'django_apscheduler',

    # Các app của bạn
    'myapp',  # Đổi thành tên ứng dụng của bạn nếu khác
]

# Định nghĩa ROOT_URLCONF (bắt buộc để tránh lỗi)
ROOT_URLCONF = 'myproject.urls'  # Đổi "myproject" thành tên thư mục chứa urls.py

# Cấu hình Database từ .env (nếu thiếu giá trị, sẽ có giá trị mặc định)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'LinguaRead'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),  # Nếu không có giá trị trong .env, mặc định là 3306
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Cấu hình Redis Cache từ .env
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}

# Định nghĩa WSGI
WSGI_APPLICATION = 'myproject.wsgi.application'

# Định nghĩa MIDDLEWARE (để Django hoạt động đúng)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Định nghĩa templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Định nghĩa static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "myapp/static"]

STATIC_ROOT = BASE_DIR / "staticfiles"