from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import json
import os
from server_data_conf.models.cluster_conf import ClusterConfig


# Create your models here.
class ClusterTableQuerySet(models.QuerySet):
    pass


class ClusterTableManager(models.Manager):
    def get_queryset(self):
        return ClusterTableQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.ClusterName.ClusterName in res.keys():
                if v.SubClusterName in res[v.ClusterName].keys():
                    res[v.ClusterName.ClusterName][v.SubClusterName].append(v.json())
                else:
                    res[v.ClusterName.ClusterName][v.SubClusterName] = [
                        v.json()
                    ]
            else:
                res[v.ClusterName.ClusterName] = {
                    v.SubClusterName: [v.json()]
                }
        return res


class ClusterTable(models.Model):
    ClusterName = models.OneToOneField(ClusterConfig, verbose_name=_('ClusterName'), on_delete=models.CASCADE)
    SubClusterName = models.CharField(_('Sub Cluster Name'), max_length=64)
    Name = models.CharField(_('Name'), max_length=64)
    Addr = models.CharField(_('Address'), max_length=32)
    Port = models.IntegerField(_('Port'))
    Weight = models.IntegerField(_('Weight'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ClusterTableManager()

    def __str__(self):
        if self.Enabled:
            return self.SubClusterName + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return self.SubClusterName + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S') + "_Disabled!!!"

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return {
            "Addr": self.Addr,
            "Name": self.Name,
            "Port": self.Port,
            "Weight": self.Weight
        }

    class Meta:
        db_table = 'ClusterTable'
        verbose_name = _('Cluster Table')
        verbose_name_plural = _('Cluster Table')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = ClusterTable.objects.get(id=self.id)
                self.pk = p.pk
            except ClusterTable.DoesNotExist:
                pass

        super(ClusterTable, self).save(*args, **kwargs)


class ClusterTableDataQuerySet(models.QuerySet):
    pass


class ClusterTableDataManager(models.Manager):
    def get_queryset(self):
        return ClusterTableDataQuerySet(self.model, using=self._db)

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
        with open(os.path.join(settings.BASE_DIR, 'conf', 'cluster_conf', 'cluster_table.data'), 'w')as file:
            file.write(json.dumps(s))


class ClusterTableData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Config = models.ManyToManyField(ClusterTable, verbose_name=_('Config'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ClusterTableDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'ClusterTableData'
        verbose_name = _('Cluster Table Data')
        verbose_name_plural = _('Cluster Table Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            ClusterTableData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = ClusterTableData.objects.get(id=self.id)
                self.pk = p.pk
            except ClusterTableData.DoesNotExist:
                pass

        super(ClusterTableData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for clusterTable in self.Config.filter(Enabled=True):
            if clusterTable.ClusterName.ClusterName in res.keys():
                if clusterTable.SubClusterName in res[clusterTable.ClusterName].keys():
                    res[clusterTable.ClusterName.ClusterName][clusterTable.SubClusterName].append(clusterTable.json())
                else:
                    res[clusterTable.ClusterName.ClusterName][clusterTable.SubClusterName] = [
                        clusterTable.json()
                    ]
            else:
                res[clusterTable.ClusterName.ClusterName] = {
                    clusterTable.SubClusterName: [clusterTable.json()]
                }
        return {
            "Version": self.__str__(),
            "Config": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'cluster_conf', 'cluster_table.data'), 'w')as file:
            file.write(json.dumps(self.json()))
