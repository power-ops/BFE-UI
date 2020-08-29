from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TlsConfConfig(AppConfig):
    name = 'tls_conf'
    verbose_name = _('TLS Config')
