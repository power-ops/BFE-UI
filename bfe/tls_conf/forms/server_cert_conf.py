from django import forms
from django.utils.translation import ugettext_lazy as _
from tls_conf.models.server_cert_conf import *


class CertForm(forms.ModelForm):
    Domain = forms.CharField(label=_('Domain'), max_length=64)
    ServerKey = forms.FileField(label=_('ServerKey'))
    ServerCert = forms.FileField(label=_('ServerCert'))

    def save(self, commit=True):
        instance = super(CertForm, self).save(commit=False)
        instance.ServerKeyName = self.cleaned_data['ServerKey']
        instance.ServerKeyData = self.cleaned_data['ServerKey'].read()
        instance.ServerCertName = self.cleaned_data['ServerCert']
        instance.ServerCertData = self.cleaned_data['ServerCert'].read()
        return instance

    class Meta:
        model = Cert
        exclude = ['CreateDate']
        fields = ['Domain', 'ServerCert', 'ServerKey', 'Enabled']


class CertDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Default = forms.CharField(label=_('Default'), max_length=64)
    CertConf = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                              queryset=Cert.objects.all())

    class Meta:
        model = CertData
        exclude = ['CreateDate']
        fields = ['Name', 'Default', 'CertConf']

    def save(self, commit=True):
        instance = super(CertDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(CertData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = CertData.objects.create(
                Name=self.instance.Name,
                Default=self.instance.Default,
                Enabled=True,
            )
            for c in self.instance.CertConf.all():
                new.CertConf.add(c)
            new.save()
            instance = CertData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
