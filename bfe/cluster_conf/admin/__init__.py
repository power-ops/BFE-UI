from django.contrib import admin
from django.conf import settings
from cluster_conf.admin.cluster_table import ClusterTableAdmin, ClusterTableDataAdmin
from cluster_conf.admin.gslb import GSLBAdmin, GSLBDataAdmin
from cluster_conf.models import cluster_table, gslb

admin.site.site_header = settings.DJANGO_TITLE
admin.site.register(cluster_table.ClusterTable, ClusterTableAdmin)
admin.site.register(cluster_table.ClusterTableData, ClusterTableDataAdmin)
admin.site.register(gslb.GSLB, GSLBAdmin)
admin.site.register(gslb.GSLBData, GSLBDataAdmin)
