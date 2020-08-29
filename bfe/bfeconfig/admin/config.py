from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from bfeconfig.forms.config import BfeConfigForm


class BfeConfigAdmin(admin.ModelAdmin):
    list_display = ('Name', 'UUID', 'Enabled', 'CreateDate')
    form = BfeConfigForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    # server_data_conf
    def getClusterConfig(self, obj):
        return obj.ClusterConfig.json()

    getClusterConfig.short_description = _('ClusterConfig')

    def getHostRule(self, obj):
        return obj.HostRule.json()

    getHostRule.short_description = _('Host Rule')

    def getNameConfig(self, obj):
        return obj.NameConfig.json()

    getNameConfig.short_description = _('NameConfig')

    def getRouteRule(self, obj):
        return obj.RouteRule.json()

    getRouteRule.short_description = _('RouteRule')

    def getVipRule(self, obj):
        return obj.VipRule.json()

    getVipRule.short_description = _('VipRule')

    # cluster_conf

    def getClusterTable(self, obj):
        return obj.ClusterTable.json()

    getClusterTable.short_description = _('ClusterTable')

    def getGSLB(self, obj):
        return obj.GSLB.json()

    getGSLB.short_description = _('GSLBData')

    # tls_conf

    def getServerCertConf(self, obj):
        return obj.ServerCertConf.json()

    getServerCertConf.short_description = _('ServerCertConf')

    def getSessionTicketKey(self, obj):
        return obj.SessionTicketKey.json()

    getSessionTicketKey.short_description = _('SessionTicketKey')

    def getTLSRuleConf(self, obj):
        return obj.TLSRuleConf.json()

    getTLSRuleConf.short_description = _('TLSRuleConf')

    # mod

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['UUID', 'CreateDate']
        self.fieldsets = (
            (None, {
                'fields': ('Name', 'UUID', 'Enabled', 'CreateDate')
            }),
            (_("server_data_conf"), {
                'fields': ('ClusterConfig', 'HostRule', 'NameConfig', 'RouteRule', 'VipRule')
            }),
            (_("cluster_conf"), {
                'fields': ('ClusterTable', 'GSLB')
            }),
            (_("tls_conf"), {
                'fields': ('ServerCertConf', 'SessionTicketKey', 'TLSRuleConf')
            }),
            (_("mod"), {
                'fields': ('')
            })
        )
        return super(BfeConfigAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'UUID', 'CreateDate',
                                'getClusterConfig', 'getHostRule', 'getNameConfig', 'getRouteRule', 'getVipRule',
                                'getClusterTable', 'getGSLB',
                                'getServerCertConf', 'getSessionTicketKey', 'getTLSRuleConf',
                                ]

        self.fieldsets = (
            (None, {
                'fields': ('Name', 'UUID', 'Enabled', 'CreateDate')
            }),
            (_("server_data_conf"), {
                'fields': (
                    'ClusterConfig', 'getClusterConfig',
                    'HostRule', 'getHostRule',
                    'NameConfig', 'getNameConfig',
                    'RouteRule', 'getRouteRule',
                    'VipRule', 'getVipRule')
            }),
            (_("cluster_conf"), {
                'fields': (
                    'ClusterTable', 'getClusterTable', 'GSLB', 'getGSLB')
            }),
            (_("tls_conf"), {
                'fields': (
                    'ServerCertConf', 'getServerCertConf',
                    'SessionTicketKey', 'getSessionTicketKey',
                    'TLSRuleConf', 'getTLSRuleConf')
            }),
            (_("mod"), {
                'fields': ('')
            })
        )
        return super(BfeConfigAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
