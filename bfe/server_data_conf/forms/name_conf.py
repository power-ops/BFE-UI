from django import forms
from django.utils.translation import ugettext_lazy as _
from server_data_conf.models.name_conf import *


class NameConfigForm(forms.ModelForm):
    Instance = forms.CharField(label=_('Instance'), max_length=64)
    Host = forms.CharField(label=_('Host'), max_length=64)
    Port = forms.IntegerField(label=_('Port'))
    Weight = forms.IntegerField(label=_('Weight'))

    class Meta:
        model = NameConfig
        exclude = ['CreateDate']
        fields = ['Instance', 'Host', 'Port', 'Weight', 'Enabled', 'CreateDate']


class NameConfigDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Config = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            queryset=NameConfig.objects.all())

    class Meta:
        model = NameConfigData
        exclude = ['CreateDate']
        fields = ['Name', 'Config']

    def save(self, commit=True):
        instance = super(NameConfigDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(NameConfigData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = NameConfigData.objects.create(Name=self.instance.Name,
                                                Enabled=True,
                                                )
            for c in self.instance.Config.all():
                new.Config.add(c)
            new.save()
            instance = NameConfigData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
