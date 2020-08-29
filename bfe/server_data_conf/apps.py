from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ServerDataConfConfig(AppConfig):
    name = 'server_data_conf'
    verbose_name = _('Server Data Config')
