from django.contrib import admin
from tls_conf.forms.tls_rule_conf import *
from django.utils.translation import ugettext_lazy as _


class TLSRuleAdmin(admin.ModelAdmin):
    list_display = ('Product', 'CertName', 'ClientCAName', 'Enabled', 'CreateDate')
    form = TLSRuleForm


class TLSRuleDataAdmin(admin.ModelAdmin):
    list_display = ('Name','DefaultNextProtos', 'Enabled', 'CreateDate')
    form = TLSRuleDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'DefaultNextProtos', 'Config', 'Enabled', 'CreateDate']
        return super(TLSRuleDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'DefaultNextProtos', 'Config', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(TLSRuleDataAdmin, self).change_view(request, object_id, form_url, extra_context)
