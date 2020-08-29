from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from server_data_conf.forms.host_rule import *


class HostTagAdmin(admin.ModelAdmin):
    list_display = ('Tag', 'Domain', 'Enabled', 'CreateDate')
    form = HostTagForm
    list_per_page = 20

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(HostTagAdmin, self).add_view(request, extra_context=None)


class HostProductAdmin(admin.ModelAdmin):
    list_display = ('Tag', 'Product', 'Enabled', 'CreateDate')
    form = HostProductForm
    list_per_page = 20

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(HostProductAdmin, self).add_view(request, extra_context=None)


class HostRuleDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'DefaultProduct', 'Enabled', 'CreateDate')
    form = HostRuleDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'DefaultProduct', 'Hosts', 'HostTags', 'Enabled', 'CreateDate']
        return super(HostRuleDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'DefaultProduct', 'Hosts', 'HostTags', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(HostRuleDataAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
