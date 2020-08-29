from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import json
import os


class ClusterConfigQuerySet(models.QuerySet):
    pass


class ClusterConfigManager(models.Manager):
    def get_queryset(self):
        return ClusterConfigQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.ClusterName in res.keys():
                # warn
                res[v.ClusterName] = v.json()
            else:
                res[v.ClusterName] = v.json()
        return res


class ClusterConfig(models.Model):
    ClusterName = models.CharField(_('Cluster Name'), max_length=64)

    # CheckConf
    Schem = models.CharField(_('Schem'), max_length=64)
    Uri = models.CharField(_('Uri'), max_length=64)
    Host = models.CharField(_('Host'), max_length=64)
    StatusCode = models.IntegerField(_('StatusCode'))

    # BackendConf
    TimeoutConnSrv = models.IntegerField(_('TimeoutConnSrv'), null=True)
    TimeoutResponseHeader = models.IntegerField(_('TimeoutResponseHeader'), null=True)
    MaxIdleConnsPerHost = models.IntegerField(_('MaxIdleConnsPerHost'), null=True)
    RetryLevel = models.IntegerField(_('RetryLevel'), null=True)

    # GslbBasic
    CrossRetry = models.IntegerField(_('CrossRetry'), null=True)
    RetryMax = models.IntegerField(_('RetryMax'), null=True)
    BalanceMode = models.CharField(_('BalanceMode'), max_length=64, null=True)
    # HashConf
    HashStrategy = models.IntegerField(_('HashStrategy'), null=True)
    HashHeader = models.IntegerField(_('HashHeader'), null=True)
    SessionSticky = models.BooleanField(_('SessionSticky'), null=True)

    # ClusterBasic
    TimeoutReadClient = models.IntegerField(_('TimeoutReadClient'), null=True)
    TimeoutWriteClient = models.IntegerField(_('TimeoutWriteClient'), null=True)
    TimeoutReadClientAgain = models.IntegerField(_('TimeoutReadClientAgain'), null=True)
    ReqWriteBufferSize = models.IntegerField(_('ReqWriteBufferSize'), null=True)
    ReqFlushInterval = models.IntegerField(_('ReqFlushInterval'), null=True)
    ResFlushInterval = models.IntegerField(_('ResFlushInterval'), null=True)
    CancelOnClientClose = models.IntegerField(_('CancelOnClientClose'), null=True)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ClusterConfigManager()

    def __str__(self):
        return self.ClusterName + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        res = {
            "CheckConf": {
                "Schem": self.Schem,
                "Uri": self.Uri,
                "Host": self.Host,
                "StatusCode": self.StatusCode
            }
        }

        BackendConf = {}
        if self.TimeoutConnSrv:
            BackendConf['TimeoutConnSrv'] = self.TimeoutConnSrv
        if self.TimeoutResponseHeader:
            BackendConf['TimeoutResponseHeader'] = self.TimeoutResponseHeader
        if self.MaxIdleConnsPerHost:
            BackendConf['MaxIdleConnsPerHost'] = self.MaxIdleConnsPerHost
        if self.RetryLevel:
            BackendConf['RetryLevel'] = self.RetryLevel
        if BackendConf:
            res['BackendConf'] = BackendConf
        GslbBasic = {}
        if self.CrossRetry:
            GslbBasic['CrossRetry'] = self.CrossRetry
        if self.RetryMax:
            GslbBasic['RetryMax'] = self.RetryMax
        HashConf = {}
        if self.HashStrategy:
            HashConf['HashStrategy'] = self.HashStrategy
        if self.HashHeader:
            HashConf['HashHeader'] = self.HashHeader
        if self.SessionSticky != None:
            HashConf['SessionSticky'] = self.SessionSticky
        if HashConf:
            GslbBasic['HashConf'] = HashConf
        if GslbBasic:
            res['GslbBasic'] = GslbBasic

        ClusterBasic = {}
        if self.TimeoutReadClient:
            ClusterBasic['TimeoutReadClient'] = self.TimeoutReadClient
        if self.TimeoutWriteClient:
            ClusterBasic['TimeoutWriteClient'] = self.TimeoutWriteClient
        if self.TimeoutReadClientAgain:
            ClusterBasic['TimeoutReadClientAgain'] = self.TimeoutReadClientAgain
        if self.ReqWriteBufferSize:
            ClusterBasic['ReqWriteBufferSize'] = self.ReqWriteBufferSize
        if self.ReqFlushInterval:
            ClusterBasic['ReqFlushInterval'] = self.ReqFlushInterval
        if self.ResFlushInterval:
            ClusterBasic['ResFlushInterval'] = self.ResFlushInterval
        if self.CancelOnClientClose:
            ClusterBasic['CancelOnClientClose'] = self.CancelOnClientClose
        if ClusterBasic:
            res['ClusterBasic'] = ClusterBasic
        return res

    class Meta:
        db_table = 'ClusterConfig'
        verbose_name = _('Cluster Config')
        verbose_name_plural = _('Cluster Config')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = ClusterConfig.objects.get(id=self.id)
                self.pk = p.pk
            except ClusterConfig.DoesNotExist:
                pass

        super(ClusterConfig, self).save(*args, **kwargs)


class ClusterConfigDataQuerySet(models.QuerySet):
    pass


class ClusterConfigDataManager(models.Manager):
    def get_queryset(self):
        return ClusterConfigDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            s = {
                "Version": "nil",
                "Config": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'cluster_conf.data'), 'w')as file:
            file.write(json.dumps(s))


class ClusterConfigData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Config = models.ManyToManyField(ClusterConfig, verbose_name=_('Config'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ClusterConfigDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'ClusterConfigData'
        verbose_name = _('Cluster Config Data')
        verbose_name_plural = _('Cluster Config Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            ClusterConfigData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = ClusterConfigData.objects.get(id=self.id)
                self.pk = p.pk
            except ClusterConfigData.DoesNotExist:
                pass
        super(ClusterConfigData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.Config.filter(Enabled=True):
            if v.ClusterName in res.keys():
                # warn
                res[v.ClusterName] = v.json()
            else:
                res[v.ClusterName] = v.json()
        return {
            "Version": self.__str__(),
            "Config": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'cluster_conf.data'), 'w')as file:
            file.write(json.dumps(self.json()))
