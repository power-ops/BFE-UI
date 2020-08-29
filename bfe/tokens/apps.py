from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TokensConfig(AppConfig):
    name = 'tokens'
    verbose_name = _('Tokens')
