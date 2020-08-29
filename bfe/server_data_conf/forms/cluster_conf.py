from django import forms
from django.utils.translation import ugettext_lazy as _
from server_data_conf.models.cluster_conf import *


class ClusterConfigForm(forms.ModelForm):
    ClusterName = forms.CharField(label=_('Cluster Name'), max_length=64, )

    # CheckConf
    schem = (
        ("http", "http"),
        ("tcp", "tcp"),
        ("udp", "udp"),
    )
    Schem = forms.ChoiceField(label=_('Schem'), choices=schem)
    Uri = forms.CharField(label=_('Uri'))
    Host = forms.CharField(label=_('Host'))
    StatusCode = forms.IntegerField(label=_('StatusCode'))

    # BackendConf
    TimeoutConnSrv = forms.IntegerField(label=_('TimeoutConnSrv'), required=False)
    TimeoutResponseHeader = forms.IntegerField(label=_('TimeoutResponseHeader'), required=False)
    MaxIdleConnsPerHost = forms.IntegerField(label=_('MaxIdleConnsPerHost'), required=False)
    RetryLevel = forms.IntegerField(label=_('RetryLevel'), required=False)

    # GslbBasic
    CrossRetry = forms.IntegerField(label=_('CrossRetry'), required=False)
    RetryMax = forms.IntegerField(label=_('RetryMax'), required=False)
    BalanceMode = forms.CharField(label=_('BalanceMode'), required=False)
    # HashConf
    HashStrategy = forms.IntegerField(label=_('HashStrategy'), required=False)
    HashHeader = forms.IntegerField(label=_('HashHeader'), required=False)
    SessionSticky = forms.NullBooleanField(label=_('SessionSticky'), required=False)

    # ClusterBasic
    TimeoutReadClient = forms.IntegerField(label=_('TimeoutReadClient'), required=False)
    TimeoutWriteClient = forms.IntegerField(label=_('TimeoutWriteClient'), required=False)
    TimeoutReadClientAgain = forms.IntegerField(label=_('TimeoutReadClientAgain'), required=False)
    ReqWriteBufferSize = forms.IntegerField(label=_('ReqWriteBufferSize'), required=False)
    ReqFlushInterval = forms.IntegerField(label=_('ReqFlushInterval'), required=False)
    ResFlushInterval = forms.IntegerField(label=_('ResFlushInterval'), required=False)
    CancelOnClientClose = forms.IntegerField(label=_('CancelOnClientClose'), required=False)

    Enabled = forms.BooleanField(required=False, initial=True)

    # CreateDate = forms.DateTimeField(label=_('Create Date'))

    class Meta:
        model = ClusterConfig
        exclude = ['CreateDate']
        # fields = ['ClusterName', 'Schem', 'Uri', 'Host', 'StatusCode', 'Enabled']


class ClusterConfigDataForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)

    Config = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            queryset=ClusterConfig.objects.all())

    class Meta:
        model = ClusterConfigData
        exclude = ['CreateDate']
        fields = ['Name', 'Config']

    def save(self, commit=True):
        instance = super(ClusterConfigDataForm, self).save(commit=False)
        if len([x for x in self.changed_data if x != 'Enabled']) > 0 and self.instance.Enabled and self.instance.id and \
                len(ClusterConfigData.objects.filter(Name=self.instance.Name).all()) > 0:
            new = ClusterConfigData.objects.create(
                Name=self.instance.Name,
                Enabled=True,
            )
            for c in self.instance.Config.all():
                new.Config.add(c)
            new.save()
            instance = ClusterConfigData.objects.get_by_id(self.instance.id)
            instance.Enabled = False
        return instance
