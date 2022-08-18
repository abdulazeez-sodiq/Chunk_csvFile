import os

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default' : {
        'Engine':'django.db.backends.sqlite3',
        'NAME' : os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}