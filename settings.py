DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'core',
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
SECRET_KEY = 'secret-key-for-development-only'
