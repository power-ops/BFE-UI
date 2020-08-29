from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ClusterConfConfig(AppConfig):
    name = 'cluster_conf'
    verbose_name = _('Cluster Config')
