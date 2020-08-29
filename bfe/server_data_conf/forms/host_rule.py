from django import forms
from django.utils.translation import ugettext_lazy as _
from server_data_conf.models.host_rule import *


class HostTagForm(forms.ModelForm):
    Tag = forms.CharField(label=_('Tag'), max_length=64)
    Domain = forms.CharField(label=_('Domain'), max_length=64)

    class Meta:
        model = HostTag
        exclude = ['CreateDate']
        fields = ['Tag', 'Domain', 'Enabled', 'CreateDate']


class HostProductForm(forms.ModelForm):
    class Meta:
        model = HostProduct
        exclude = ['CreateDate']
        fields = ['Product', 'Tag', 'Enabled', 'CreateDate']


class HostRuleDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    DefaultProduct = forms.CharField(required=False, label=_('Default Product'), max_length=64)
    Hosts = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                           queryset=HostProduct.objects.all())
    HostTags = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                              queryset=HostTag.objects.all())

    class Meta:
        model = HostRuleData
        exclude = ['CreateDate']
        fields = ['Name', 'DefaultProduct']

    def save(self, commit=True):
        instance = super(HostRuleDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(HostRuleData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = HostRuleData.objects.create(
                Name=self.instance.Name,
                DefaultProduct=self.instance.DefaultProduct,
                Enabled=True,
            )
            for c in self.instance.Hosts.all():
                new.Hosts.add(c)
            for c in self.instance.HostTags.all():
                new.HostTags.add(c)
            new.save()
            instance = HostRuleData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
