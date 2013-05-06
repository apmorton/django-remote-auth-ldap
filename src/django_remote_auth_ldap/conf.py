from django.conf import settings  # noqa
from appconf import AppConf


class DjangoRemoteAuthLdapAppConf(AppConf):
    CHECK_DOMAIN = True
    STRIP_DOMAIN = True
    DOMAINS = []
    HEADER = 'REMOTE_USER'

    class Meta:
        prefix = 'DRAL'
