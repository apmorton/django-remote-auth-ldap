Django Remote Auth LDAP
=========================

[![Build Status](https://travis-ci.org/Juvenal1228/django-remote-auth-ldap.png?branch=master)](https://travis-ci.org/Juvenal1228/django-remote-auth-ldap)

Purpose
-------

This app combines [django-auth-ldap](http://pythonhosted.org/django-auth-ldap/) with django's [RemoteUserBackend](https://docs.djangoproject.com/en/dev/howto/auth-remote-user/)
It allows django applications hosted in IIS to take advantage of Windows Authentication in IIS (401 Challenge) while also having the advanced features offered in `django-auth-ldap`


Features
--------

- [PEP 8](http://www.python.org/dev/peps/pep-0008/) compliance
- [semver](http://semver.org/) compliance


Installing
----------

Install with pip/easy_install from the pypi

`pip install django-remote-auth-ldap`

or clone the latest source

    git clone https://github.com/Juvenal1228/django-remote-auth-ldap.git
    cd django-remote-auth-ldap
    python setup.py install


Using
-----

In your django settings.py file configure django-auth-ldap normally, verify that the configuration is indeed working!

Add the `RemoteUserMiddleware` class after the `AuthenticationMiddleware` class
```python
MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_remote_auth_ldap.middleware.RemoteUserMiddleware',
    ...
)
```

Set the RemoteUserLDAPBackend as the authentication backend
```python
AUTHENTICATION_BACKENDS = (
    'django_remote_auth_ldap.backend.RemoteUserLDAPBackend',
)
```

The application expects the remote user to be in the form `domain\user` (which is how IIS returns it)

Settings
--------

There are a few settings you can use to control the behavior

- `DRAL_CHECK_DOMAIN` - Boolean - whether or not to check the domain against a known list - default True
- `DRAL_STRIP_DOMAIN` - Boolean - whether or not to strip the domain off the username before passing to django-auth-ldap - default True
- `DRAL_DOMAINS` - List - list of domains to check against, should be lowercase! - default []
- `DRAL_HEADER` - String - header to check for remote user in - default REMOTE_USER


