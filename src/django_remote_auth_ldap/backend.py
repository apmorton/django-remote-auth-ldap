from django.contrib.auth.backends import RemoteUserBackend

from django_auth_ldap.backend import LDAPBackend, _LDAPUser
from django_remote_auth_ldap.conf import settings


class RemoteUserLDAPBackend(LDAPBackend):
    # unforgivable megahax to avoid reimplementing RemoteUserMiddleware
    __class__ = RemoteUserBackend

    def authenticate(self, remote_user):
        if not self.correct_domain(remote_user):
            return None

        username = self.clean_username(remote_user)
        ldap_user = RemoteLDAPUser(self, username=username)
        user = ldap_user.authenticate('')

        return user

    def correct_domain(self, username):
        if not settings.DRAL_CHECK_DOMAIN:
            return True
        if not '\\' in username:
            return False
        (dom, username) = username.split('\\', 1)
        return dom.lower() in settings.DRAL_DOMAINS

    def clean_username(self, username):
        if not settings.DRAL_STRIP_DOMAIN:
            return username
        if not '\\' in username:
            return username
        (dom, username) = username.split('\\', 1)
        return username


class RemoteLDAPUser(_LDAPUser):
    def _authenticate_user_dn(self, password):
        if self.dn is None:
            msg = "Failed to map the username to a DN."
            raise self.AuthenticationFailed(msg)
