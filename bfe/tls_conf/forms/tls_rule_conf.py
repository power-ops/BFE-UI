from django import forms
from django.utils.translation import ugettext_lazy as _
from tls_conf.models.tls_rule_conf import *


class TLSRuleForm(forms.ModelForm):
    VipConf = forms.CharField(label=_('VipConf'), widget=forms.Textarea)
    SniConf = forms.CharField(label=_('SniConf'), max_length=64, required=False)
    CertName = forms.CharField(label=_('CertName'), max_length=64)
    NextProtos = forms.CharField(label=_('NextProtos'), widget=forms.Textarea)
    Grade = forms.CharField(label=_('Grade'), max_length=64)
    ClientCAName = forms.CharField(label=_('ClientCAName'), max_length=64)

    class Meta:
        model = TLSRule
        exclude = ['CreateDate']
        fields = ['Product', 'VipConf', 'SniConf', 'CertName', 'NextProtos', 'Grade', 'ClientCAName', 'Enabled']


class TLSRuleDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    DefaultNextProtos = forms.CharField(label=_('DefaultNextProtos'), widget=forms.Textarea)

    Config = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            queryset=TLSRule.objects.all())

    class Meta:
        model = TLSRuleData
        exclude = ['CreateDate']
        fields = ['Name', 'DefaultNextProtos', 'Config']

    def save(self, commit=True):
        instance = super(TLSRuleDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(TLSRuleData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = TLSRuleData.objects.create(Name=self.instance.Name,
                                             Enabled=True,
                                             )
            for c in self.instance.Config.all():
                new.Config.add(c)
            new.save()
            instance = TLSRuleData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
