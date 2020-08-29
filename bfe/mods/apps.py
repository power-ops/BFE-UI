from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ModsConfig(AppConfig):
    name = 'mods'
    verbose_name = _('Mods')
