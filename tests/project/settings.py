import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'dumb'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'tests.project.app'
]

MIDDLEWARE = []

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'TEST': {'NAME': ':memory:'}
    }
}

ENVIRONMENT = "dev"
