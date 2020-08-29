from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from server_data_conf.forms.vip_rule import *


class VipRuleAdmin(admin.ModelAdmin):
    list_display = ('Product2Vip', 'VipList', 'Enabled', 'CreateDate')
    form = VipRuleForm
    list_per_page = 20

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        return super(VipRuleAdmin, self).add_view(request, extra_context=None)


class VipRuleDataAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CreateDate')
    form = VipRuleDataForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'Vips', 'Enabled', 'CreateDate']
        return super(VipRuleDataAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'Vips', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(VipRuleDataAdmin, self).change_view(request, object_id, form_url, extra_context)

    # def has_change_permission(self, request, obj=None):
    #     """ 取消后台修改功能 """
    #     return False
