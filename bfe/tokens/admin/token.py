from django.contrib import admin
from tokens.forms.token import TokenForm
from django.utils.translation import ugettext_lazy as _


class TokenAdmin(admin.ModelAdmin):
    list_display = ('AppName', 'TokenId', 'Comment', 'Enabled', 'CreateDate')
    form = TokenForm
    list_filter = ('AppName', 'Enabled')
    list_per_page = 20
    search_fields = ['AppName', 'TokenId']

    # server_data_conf
    def getClusterConfig(self, obj):
        return obj.BfeConfig.ClusterConfig.json()

    getClusterConfig.short_description = _('ClusterConfig')

    def getHostRule(self, obj):
        return obj.BfeConfig.HostRule.json()

    getHostRule.short_description = _('Host Rule')

    def getNameConfig(self, obj):
        return obj.BfeConfig.NameConfig.json()

    getNameConfig.short_description = _('NameConfig')

    def getRouteRule(self, obj):
        return obj.BfeConfig.RouteRule.json()

    getRouteRule.short_description = _('RouteRule')

    def getVipRule(self, obj):
        return obj.BfeConfig.VipRule.json()

    getVipRule.short_description = _('VipRule')

    # cluster_conf

    def getClusterTable(self, obj):
        return obj.BfeConfig.ClusterTable.json()

    getClusterTable.short_description = _('ClusterTable')

    def getGSLB(self, obj):
        return obj.BfeConfig.GSLB.json()

    getGSLB.short_description = _('GSLBData')

    # tls_conf

    def getServerCertConf(self, obj):
        return obj.BfeConfig.ServerCertConf.json()

    getServerCertConf.short_description = _('ServerCertConf')

    def getSessionTicketKey(self, obj):
        return obj.BfeConfig.SessionTicketKey.json()

    getSessionTicketKey.short_description = _('SessionTicketKey')

    def getTLSRuleConf(self, obj):
        return obj.BfeConfig.TLSRuleConf.json()

    getTLSRuleConf.short_description = _('TLSRuleConf')

    # mod

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.exclude = ['TokenId']
        self.fieldsets = []
        return super(TokenAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['TokenId', 'CreateDate', 'AppName',
                                'getClusterConfig', 'getHostRule', 'getNameConfig', 'getRouteRule', 'getVipRule',
                                'getClusterTable', 'getGSLB',
                                'getServerCertConf', 'getSessionTicketKey', 'getTLSRuleConf',
                                ]
        self.fieldsets = (
            (None, {
                'fields': ('AppName', 'TokenId', 'BfeConfig', 'Comment', 'Enabled', 'CreateDate')
            }),
            (_("server_data_conf"), {
                'fields': ('getClusterConfig', 'getHostRule', 'getNameConfig', 'getRouteRule', 'getVipRule')
            }),
            (_("cluster_conf"), {
                'fields': ('getClusterTable', 'getGSLB')
            }),
            (_("tls_conf"), {
                'fields': ('getServerCertConf', 'getSessionTicketKey', 'getTLSRuleConf')
            }),
            (_("mod"), {
                'fields': ('')
            })
        )

        return super(TokenAdmin, self).change_view(request, object_id, form_url, extra_context)
    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
