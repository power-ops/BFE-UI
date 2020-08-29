from django.contrib import admin
from tls_conf.forms.session_ticket_key import *
from django.utils.translation import ugettext_lazy as _


class SessionTicketKeyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'SessionTicketKey', 'CreateDate')
    form = SessionTicketKeyForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']

    def ShowMeta(self, obj):
        return obj.json()

    ShowMeta.short_description = _('Meta')

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['CreateDate']
        self.fields = ['Name', 'SessionTicketKey', 'Enabled', 'CreateDate']
        return super(SessionTicketKeyAdmin, self).add_view(request, extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['Name', 'ShowMeta', 'CreateDate']
        self.fields = ['Name', 'SessionTicketKey', 'ShowMeta', 'Enabled', 'CreateDate']
        return super(SessionTicketKeyAdmin, self).change_view(request, object_id, form_url, extra_context)
