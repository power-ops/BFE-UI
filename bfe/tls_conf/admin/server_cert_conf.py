from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tls_conf.forms.server_cert_conf import *


class CertAdmin(admin.ModelAdmin):
    list_display = ('Domain', 'ServerCertName', 'ServerKeyName', 'Enabled', 'CreateDate')
    form = CertForm
    search_fields = ['Domain', 'ServerCertName', 'ServerKeyName']
    list_filter = ('Enabled',)

    def getServerCertData(self, obj):
        return obj.ServerCertData.decode('utf-8')

    getServerCertData.short_description = _('ServerCertData')

    def getServerKeyData(self, obj):
        return obj.ServerKeyData.decode('utf-8')

    getServerKeyData.short_description = _('ServerKeyData')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fieldsets = (
            (None, {
                'fields': ('Domain', 'Enabled', 'CreateDate')
            }),
            (_('ServerCert'), {
                'fields': ('ServerCert',)
            }),
            (_('ServerKey'), {
                'fields': ('ServerKey',)
            }),
        )
        return super(CertAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fieldsets = (
            (None, {
                'fields': ('Domain', 'Enabled', 'CreateDate')
            }),
            (_('ServerCert'), {
                'fields': ('ServerCertName', 'getServerCertData',)
            }),
            (_('ServerKey'), {
                'fields': ('ServerKeyName', 'getServerKeyData')
            }),
        )
        return super(CertAdmin, self).change_view(request, object_id, form_url, extra_context)

    def has_change_permission(self, request, obj=None):
        """ 取消后台修改功能 """
        return False


class CertDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Default', 'Enabled', 'CreateDate')
    form = CertDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Default', 'CertConf', 'Enabled', 'CreateDate']
        return super(CertDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Default', 'CertConf', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(CertDataAdmin, self).change_view(request, object_id, form_url, extra_context)
