from django import forms
from django.utils.translation import ugettext_lazy as _
from server_data_conf.models.route_rule import *


class RouteRuleForm(forms.ModelForm):
    Cond = forms.CharField(label=_('Cond'), max_length=64)

    class Meta:
        model = RouteRule
        exclude = ['CreateDate']
        fields = ['Porduct', 'Cond', 'ClusterName', 'Enabled', 'CreateDate']


class RouteRuleDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    RouteRule = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                               queryset=RouteRule.objects.all())

    class Meta:
        model = RouteRuleData
        exclude = ['CreateDate']
        fields = ['Name', 'RouteRule']

    def save(self, commit=True):
        instance = super(RouteRuleDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(RouteRuleData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = RouteRuleData.objects.create(Name=self.instance.Name,
                                               Enabled=True,
                                               )
            for c in self.instance.RouteRule.all():
                new.RouteRule.add(c)
            new.save()
            instance = RouteRuleData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
