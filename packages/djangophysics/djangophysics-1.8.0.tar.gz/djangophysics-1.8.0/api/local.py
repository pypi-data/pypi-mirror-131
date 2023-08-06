SECRET_KEY = '*<J=l(+V&y=2245V6(93DRjz-V$r6Jdic8S5j8.<?%!gz:XTklBo+5Z-zPI]v9,K'

ALLOWED_HOSTS = ['127.0.0.1', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'api-dev-debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'geocurrency',
        'HOST': '127.0.0.1',
        'USER': 'geocurrency',
        'PASSWORD': 'uREfaXY7mCEaFui64eK8MY6KEYmXbrlp'
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "countries": {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'countries',
        'TIMEOUT': None
    }
}



DEBUG = True
MEDIA_ROOT = '/home/laaapin/doc/physics/media'
STATIC_ROOT = '/home/laaapin/doc/physics/static'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GEOCURRENCY_PREFIXED_UNITS_DISPLAY = {
    'meter': ['milli', 'centi', 'kilo'],
    'gram': ['milli', 'kilo'],
    'second': ['micro', 'milli'],
    'ampere': ['milli'],
    'watt_hour': ['kilo']
}
APISTAT_EXCLUDED_DOMAINS = ['admin', 'swagger']
