import logging
import os
import sys

import ldap
import slapdtest
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.cache import cache
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django_auth_ldap.config import LDAPSearch
from parameterized import parameterized

from django_remote_auth_ldap import middleware


class LDAPTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LDAPTest, cls).setUpClass()
        cls.server = slapdtest.SlapdObject()
        cls.server.suffix = 'o=test'
        cls.server.openldap_schema_files = [
            'core.schema',
            'cosine.schema',
            'inetorgperson.schema',
            'nis.schema',
        ]
        cls.server.start()
        ldif_file = os.path.normpath(os.path.join(__file__, '..', 'tests.ldif'))
        with open(ldif_file) as fp:
            ldif = fp.read()
        cls.server.ldapadd(ldif)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        super(LDAPTest, cls).tearDownClass()

    def setUp(self):
        super(LDAPTest, self).setUp()
        cache.clear()
        ldap_config = override_settings(
            AUTH_LDAP_SERVER_URI=self.server.ldap_uri,
            AUTH_LDAP_USER_SEARCH=LDAPSearch(
                'ou=people,o=test', ldap.SCOPE_SUBTREE, '(uid=%(user)s)'
            ),
        )
        ldap_config.enable()
        self.addCleanup(ldap_config.disable)

    def test_setting_DRAL_HEADER_user_in_custom_header_is_authenticated(self):
        with self.settings(DRAL_HEADER='CUSTOM', DRAL_CHECK_DOMAIN=False):
            m = middleware.RemoteUserMiddleware()
            headers = {'CUSTOM': 'alice'}
            request = RequestFactory().get('/', **headers)
            SessionMiddleware().process_request(request)
            AuthenticationMiddleware().process_request(request)
            m.process_request(request)
            self.assertIsNotNone(get_user_model().objects.get(username='alice'))

    @parameterized.expand(('alice', 'alice@test', r"test\alice"))
    def test_setting_DRAL_DOMAINS_empty_user_is_not_authenticated(self, user):
        with self.settings(DRAL_DOMAINS=[], DRAL_CHECK_DOMAIN=True):
            user = authenticate(remote_user=user)
            self.assertIsNone(user)

    def test_setting_DRAL_DOMAINS_user_with_correct_domain_is_authenticated(self):
        with self.settings(DRAL_DOMAINS=['test'], DRAL_CHECK_DOMAIN=True):
            user = authenticate(remote_user=r"test\alice")
            self.assertEqual(user.username, 'alice')

    @parameterized.expand(('alice', 'alice@test', r"fizz\alice"))
    def test_setting_DRAL_DOMAINS_user_with_incorrect_domain_is_not_authenticated(
        self, user
    ):
        with self.settings(DRAL_DOMAINS=['test'], DRAL_CHECK_DOMAIN=True):
            user = authenticate(remote_user=user)
            self.assertIsNone(user)

    def test_setting_DRAL_STRIP_DOMAIN_user_with_domain_is_not_authenticated(self):
        with self.settings(
            DRAL_STRIP_DOMAIN=False, DRAL_DOMAINS=['test'], DRAL_CHECK_DOMAIN=True
        ):
            user = authenticate(remote_user=r"test\alice")
            self.assertIsNone(user)

    def test_setting_DRAL_STRIP_DOMAIN_user_without_domain_is_authenticated(self):
        with self.settings(DRAL_STRIP_DOMAIN=False, DRAL_CHECK_DOMAIN=False):
            user = authenticate(remote_user='alice')
            self.assertEqual(user.username, 'alice')
