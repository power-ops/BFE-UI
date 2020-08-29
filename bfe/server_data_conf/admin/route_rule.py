from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from server_data_conf.forms.route_rule import *


class RouteRuleAdmin(admin.ModelAdmin):
    list_display = ('Porduct', 'ClusterName', 'Cond', 'Enabled', 'CreateDate')
    form = RouteRuleForm
    list_per_page = 20

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(RouteRuleAdmin, self).add_view(request, extra_context=None)


class RouteRuleDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CreateDate')
    form = RouteRuleDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'RouteRule', 'Enabled', 'CreateDate']
        return super(RouteRuleDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'RouteRule', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(RouteRuleDataAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
