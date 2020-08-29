from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from server_data_conf.models.cluster_conf import ClusterConfig
from cluster_conf.models.cluster_table import ClusterTable
from django.conf import settings
import json
import os


class GSLBQuerySet(models.QuerySet):
    pass


class GSLBManager(models.Manager):
    def get_queryset(self):
        return GSLBQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.ClusterName.ClusterName in res.keys():
                res[v.ClusterName.ClusterName].append(v.json())
            else:
                res[v.ClusterName.ClusterName] = v.json()
        return res


class GSLB(models.Model):
    ClusterName = models.OneToOneField(ClusterConfig, verbose_name=_('ClusterName'), on_delete=models.CASCADE)
    SubClusterName = models.CharField(_('Sub Cluster Name'), max_length=64)
    Blackhole = models.IntegerField(_('GSLB BLACKHOLE'))
    Weight = models.IntegerField(_('Weight'))
    ClusterSubName = models.OneToOneField(ClusterTable, verbose_name=_('Cluster Sub Name'), on_delete=models.CASCADE)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = GSLBManager()

    # def __str__(self):
    #     return self.SubClusterName + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return {
            "GSLB_BLACKHOLE": self.Blackhole,
            self.ClusterSubName.SubClusterName: self.Weight,
        }

    class Meta:
        db_table = 'GSLB'
        verbose_name = _('GSLB')
        verbose_name_plural = _('GSLB')

    def save(self, *args, **kwargs):
        self.ClusterName = self.ClusterSubName.ClusterName
        if not self.pk:
            try:
                p = GSLB.objects.get(id=self.id)
                self.pk = p.pk
            except GSLB.DoesNotExist:
                pass

        super(GSLB, self).save(*args, **kwargs)


class GSLBDataQuerySet(models.QuerySet):
    pass


class GSLBDataManager(models.Manager):
    def get_queryset(self):
        return GSLBDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = {
                "Version": data.Version + "_" + data.CreateDate.strftime('%Y-%m-%d %H:%M:%S'),
                "Hostname": data.Hostname,
                "Ts": data.Ts,
                "Clusters": json.loads(data.Clusters),
            }
        else:
            s = {
                "Version": "nil",
                "Hostname": "",
                "Ts": "0",
                "Clusters": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'cluster_conf', 'gslb.data'), 'w')as file:
            file.write(json.dumps(s))


class GSLBData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Hostname = models.CharField(_('Hostname'), max_length=64, default="")
    Ts = models.CharField(_('Ts'), max_length=64)
    Clusters = models.ManyToManyField(GSLB, verbose_name=_('Clusters'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = GSLBDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'GSLBData'
        verbose_name = _('GSLB Data')
        verbose_name_plural = _('GSLB Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            GSLBData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = GSLBData.objects.get(id=self.id)
                self.pk = p.pk
            except GSLBData.DoesNotExist:
                pass

        super(GSLBData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.Clusters.filter(Enabled=True):
            if v.ClusterName.ClusterName in res.keys():
                res[v.ClusterName.ClusterName].append(v.json())
            else:
                res[v.ClusterName.ClusterName] = v.json()
        return {
            "Version": self.__str__(),
            "Hostname": self.Hostname,
            "Ts": self.Ts,
            "Clusters": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'cluster_conf', 'gslb.data'), 'w')as file:
            file.write(json.dumps(self.json()))
