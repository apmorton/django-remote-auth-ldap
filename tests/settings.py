SECRET_KEY = 'fizz'
INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests',
)
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
AUTHENTICATION_BACKENDS = ('django_remote_auth_ldap.backend.RemoteUserLDAPBackend',)
