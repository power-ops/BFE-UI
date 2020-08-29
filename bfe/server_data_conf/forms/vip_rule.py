from django import forms
from django.utils.translation import ugettext_lazy as _
from server_data_conf.models.vip_rule import *


class VipRuleForm(forms.ModelForm):
    Product2Vip = forms.CharField(label=_('Product2Vip'), max_length=64)
    VipList = forms.CharField(label=_('VipList'), widget=forms.Textarea)

    class Meta:
        model = VipRule
        exclude = ['CreateDate']
        fields = ['Product2Vip', 'VipList', 'Enabled', 'CreateDate']


class VipRuleDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Vips = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                          queryset=VipRule.objects.all())

    class Meta:
        model = VipRuleData
        exclude = ['CreateDate']
        fields = ['Name', 'Vips']

    def save(self, commit=True):
        instance = super(VipRuleDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(VipRuleData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = VipRuleData.objects.create(Name=self.instance.Name,
                                             Enabled=True,
                                             )
            for c in self.instance.Vips.all():
                new.Vips.add(c)
            new.save()
            instance = VipRuleData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
