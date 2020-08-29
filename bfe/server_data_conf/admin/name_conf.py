from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from server_data_conf.forms.name_conf import *


class NameConfigAdmin(admin.ModelAdmin):
    list_display = ('Instance', 'Host', 'Port', 'Weight', 'Enabled', 'CreateDate')
    form = NameConfigForm
    list_per_page = 20

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(NameConfigAdmin, self).add_view(request, extra_context=None)


class NameConfigDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CreateDate')
    form = NameConfigDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Config', 'Enabled', 'CreateDate']
        return super(NameConfigDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Config', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(NameConfigDataAdmin, self).change_view(request, object_id, form_url, extra_context)
    #
    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
