
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass



# 測試
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdb',
        'USER': 'root',
        'PASSWORD': '54152067',
        'HOST': '192.168.1.105',
        'PORT': '3306',
    }
}



'''
# 生產
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'asset',
        'USER': 'root',
        'PASSWORD': '54152067',
        'HOST': '192.168.1.105',
        'PORT': '3306',
    }
}
'''

STATIC_ROOT = 'static'
DEBUG = False
