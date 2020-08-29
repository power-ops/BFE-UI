from django import forms
from django.utils.translation import ugettext_lazy as _
from cluster_conf.models.gslb import *


class GSLBForm(forms.ModelForm):
    Blackhole = forms.IntegerField(label=_('GSLB BLACKHOLE'))
    Weight = forms.IntegerField(label=_('Weight'))
    Enabled = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = GSLB
        exclude = ['CreateDate']
        fields = ['ClusterName', 'Blackhole', 'ClusterSubName', 'Weight', 'Enabled']


class GSLBDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Hostname = forms.CharField(label=_('Hostname'), max_length=64, required=False)
    Ts = forms.CharField(label=_('Ts'), max_length=64)
    Clusters = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                              queryset=GSLB.objects.all())

    class Meta:
        model = GSLBData
        exclude = ['CreateDate']

    def save(self, commit=True):
        instance = super(GSLBDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(GSLBData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = GSLBData.objects.create(Name=self.instance.Name,
                                          Hostname=self.instance.Hostname,
                                          Ts=self.instance.Ts,
                                          Enabled=True,
                                          )
            for c in self.instance.Clusters.all():
                new.Clusters.add(c)
            new.save()
            instance = GSLBData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
