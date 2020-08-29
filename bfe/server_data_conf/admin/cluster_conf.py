from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from server_data_conf.forms.cluster_conf import *


class ClusterConfigAdmin(admin.ModelAdmin):
    list_display = ('ClusterName', 'Schem', 'Uri', 'Host', 'StatusCode', 'Enabled', 'CreateDate')
    form = ClusterConfigForm
    fieldsets = (
        (None, {
            'fields': ('ClusterName', 'Enabled', 'CreateDate')
        }),
        (_("CheckConf"), {
            'fields': ('Schem', 'Uri', 'Host', 'StatusCode')
        }),
        (_("BackendConf"), {
            'classes': ('collapse',),
            'fields': ('TimeoutConnSrv', 'TimeoutResponseHeader', 'MaxIdleConnsPerHost', 'RetryLevel')
        }),
        (_("GslbBasic"), {
            'classes': ('collapse',),
            'fields': ('CrossRetry', 'RetryMax', 'BalanceMode')
        }),
        (_("HashConf"), {
            'classes': ('collapse',),
            'fields': ('HashStrategy', 'HashHeader', 'SessionSticky')
        }),
        (_("ClusterBasic"), {
            'classes': ('collapse',),
            'fields': ('TimeoutReadClient', 'TimeoutWriteClient', 'TimeoutReadClientAgain', 'ReqWriteBufferSize',
                       'ReqFlushInterval', 'ResFlushInterval', 'CancelOnClientClose')
        })
    )
    readonly_fields = ('CreateDate',)

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(ClusterConfigAdmin, self).add_view(request, extra_context=None)


class ClusterConfigDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CreateDate')
    form = ClusterConfigDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Config', 'Enabled', 'CreateDate']
        return super(ClusterConfigDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Config', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(ClusterConfigDataAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
