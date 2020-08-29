from django.contrib import admin
from cluster_conf.forms.cluster_table import *
from django.utils.translation import ugettext_lazy as _


class ClusterTableAdmin(admin.ModelAdmin):
    list_display = ('ClusterName', 'SubClusterName', 'Name', 'Enabled', 'CreateDate')
    form = ClusterTableForm


class ClusterTableDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Enabled', 'CreateDate')
    form = ClusterTableDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Config', 'Enabled', 'CreateDate']
        return super(ClusterTableDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Config', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(ClusterTableDataAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
