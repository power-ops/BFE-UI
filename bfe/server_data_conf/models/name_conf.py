from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import json
import os


class NameConfigQuerySet(models.QuerySet):
    pass


class NameConfigManager(models.Manager):
    def get_queryset(self):
        return NameConfigQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Instance in res.keys():
                # warn
                res[v.Instance].append(v.json())
            else:
                res[v.Instance] = [v.json()]
        return res


class NameConfig(models.Model):
    Instance = models.CharField(_('Instance'), max_length=64)
    Host = models.CharField(_('Host'), max_length=64)
    Port = models.IntegerField(_('Port'))
    Weight = models.IntegerField(_('Weight'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = NameConfigManager()

    def __str__(self):
        return self.Instance + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        return {
            "Host": self.Host,
            "Port": self.Port,
            "Weight": self.Weight,
        }

    class Meta:
        db_table = 'NameConfig'
        verbose_name = _('Name Config')
        verbose_name_plural = _('Name Config')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = NameConfig.objects.get(id=self.id)
                self.pk = p.pk
            except NameConfig.DoesNotExist:
                pass

        super(NameConfig, self).save(*args, **kwargs)


class NameConfigDataQuerySet(models.QuerySet):
    pass


class NameConfigDataManager(models.Manager):
    def get_queryset(self):
        return NameConfigDataQuerySet(self.model, using=self._db)

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
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'name_conf.data'), 'w')as file:
            file.write(json.dumps(s))


class NameConfigData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Config = models.ManyToManyField(NameConfig, verbose_name=_('Config'), default=None)
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = NameConfigDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'NameConfigData'
        verbose_name = _('Name Config Data')
        verbose_name_plural = _('Name Config Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            NameConfigData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = NameConfigData.objects.get(id=self.id)
                self.pk = p.pk
            except NameConfigData.DoesNotExist:
                pass
        super(NameConfigData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.Config.filter(Enabled=True):
            if v.Instance in res.keys():
                # warn
                res[v.Instance].append(v.json())
            else:
                res[v.Instance] = [v.json()]
        return {
            "Version": self.__str__(),
            "Config": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'name_conf.data'), 'w')as file:
            file.write(json.dumps(self.json()))
