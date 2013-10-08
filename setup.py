from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


version = '0.1.4'

install_requires = [
    'django-auth-ldap',
    'django-appconf'
]

setup(
    name='django-remote-auth-ldap',
    version=version,
    description="REMOTE_USER authentication using LDAP",
    long_description=README,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='',
    author='Austin Morton',
    author_email='amorton@juvsoft.com',
    url='https://github.com/apmorton/django-remote-auth-ldap',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=install_requires,
    test_suite='nose.collector'
)
