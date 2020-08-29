from django.contrib import admin
from cluster_conf.forms.gslb import *
from django.utils.translation import ugettext_lazy as _


class GSLBAdmin(admin.ModelAdmin):
    list_display = ('ClusterName', 'SubClusterName', 'Blackhole', 'Weight', 'Enabled', 'CreateDate')
    form = GSLBForm


class GSLBDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Hostname', 'Ts', 'Enabled', 'CreateDate')
    form = GSLBDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Hostname', 'Ts', 'Clusters', 'Enabled', 'CreateDate']
        return super(GSLBDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Hostname', 'Ts', 'Clusters', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(GSLBDataAdmin, self).change_view(request, object_id, form_url, extra_context)
    #
    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
