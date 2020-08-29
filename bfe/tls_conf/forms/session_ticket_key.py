from django import forms
from django.utils.translation import ugettext_lazy as _
from tls_conf.models.session_ticket_key import *


class SessionTicketKeyForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    SessionTicketKey = forms.CharField(label=_('SessionTicketKey'), widget=forms.Textarea)

    class Meta:
        model = SessionTicketKey
        exclude = ['CreateDate']
        fields = ['Name', 'SessionTicketKey']

    def save(self, commit=True):
        instance = super(SessionTicketKeyForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(SessionTicketKey.objects.filter(Name=self.instance.Name).all()) > 0:
            SessionTicketKey.objects.create(Name=self.instance.Name,
                                            SessionTicketKey=self.instance.SessionTicketKey,
                                            Enabled=True,
                                            ).save()
            instance = SessionTicketKey.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
