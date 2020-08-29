from django import forms
from django.utils.translation import ugettext_lazy as _
from bfeconfig.models import *


class BfeConfigForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)

    class Meta:
        model = BfeConfig
        exclude = ['CreateDate']

    def save(self, commit=True):
        instance = super(BfeConfigForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(BfeConfig.objects.filter(Name=self.instance.Name).all()) > 0:
            if self.instance.id:
                BfeConfig.objects.create(
                    Name=self.instance.Name,
                    UUID=self.instance.UUID,
                    ClusterConfig=self.instance.ClusterConfig,
                    HostRule=self.instance.HostRule,
                    NameConfig=self.instance.NameConfig,
                    RouteRule=self.instance.RouteRule,
                    VipRule=self.instance.VipRule,
                    ClusterTable=self.instance.ClusterTable,
                    GSLB=self.instance.GSLB,
                    ServerCertConf=self.instance.ServerCertConf,
                    SessionTicketKey=self.instance.SessionTicketKey,
                    TLSRuleConf=self.instance.TLSRuleConf,
                    Enabled=True,
                ).save()
                instance = BfeConfig.objects.get_by_id(self.instance.id)
                instance.Enabled = False
            else:
                instance.UUID = BfeConfig.objects.get_by_appname(Name=self.instance.Name)[0].UUID

        return instance
