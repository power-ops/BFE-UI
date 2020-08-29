from django import forms
from django.utils.translation import ugettext_lazy as _
from cluster_conf.models.cluster_table import *


class ClusterTableForm(forms.ModelForm):
    SubClusterName = forms.CharField(label=_('Sub Cluster Name'), max_length=64)
    Name = forms.CharField(label=_('Name'), max_length=64)
    Addr = forms.CharField(label=_('Address'), max_length=32)
    Port = forms.IntegerField(label=_('Port'))
    Weight = forms.IntegerField(label=_('Weight'))
    Enabled = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = ClusterTable
        exclude = ['CreateDate']
        fields = ['ClusterName', 'SubClusterName', 'Name', 'Addr', 'Port', 'Weight', 'Enabled']


class ClusterTableDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Config = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            queryset=ClusterTable.objects.all())

    class Meta:
        model = ClusterTableData
        exclude = ['CreateDate']
        fields = ['Name', 'Config']

    def save(self, commit=True):
        instance = super(ClusterTableDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(ClusterTableData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = ClusterTableData.objects.create(Name=self.instance.Name,
                                                  Enabled=True,
                                                  )
            for c in self.instance.Cluster.all():
                new.Cluster.add(c)
            new.save()
            instance = ClusterTableData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
