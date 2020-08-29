from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from server_data_conf.models.cluster_conf import ClusterConfig
from product.models import Product
from django.conf import settings
import json
import os


class RouteRuleQuerySet(models.QuerySet):
    pass


class RouteRuleManager(models.Manager):
    def get_queryset(self):
        return RouteRuleQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Porduct.Name in res.keys():
                res[v.Porduct.Name].append(v.json())
            else:
                res[v.Porduct.Name] = [
                    v.json()
                ]
        return res


class RouteRule(models.Model):
    Porduct = models.ForeignKey(Product, verbose_name=_('Porduct'), on_delete=models.CASCADE)
    ClusterName = models.OneToOneField(ClusterConfig, verbose_name=_('ClusterName'), on_delete=models.CASCADE)
    Cond = models.CharField(_('Cond'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = RouteRuleManager()

    # ClusterName = models.OneToOneField
    def __str__(self):
        return self.Porduct.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return {
            "Cond": self.Cond,
            "ClusterName": self.ClusterName.ClusterName,
        }

    class Meta:
        db_table = 'RouteRule'
        verbose_name = _('Route Rule')
        verbose_name_plural = _('Route Rule')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = RouteRule.objects.get(id=self.id)
                self.pk = p.pk
            except RouteRule.DoesNotExist:
                pass

        super(RouteRule, self).save(*args, **kwargs)


class RouteRuleDataQuerySet(models.QuerySet):
    pass


class RouteRuleDataManager(models.Manager):
    def get_queryset(self):
        return RouteRuleDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            s = {
                "Version": "nil",
                "ProductRule": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'route_rule.data'), 'w')as file:
            file.write(json.dumps(s))


class RouteRuleData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    RouteRule = models.ManyToManyField(RouteRule, verbose_name=_('RouteRule'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = RouteRuleDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'RouteRuleData'
        verbose_name = _('Route Rule Data')
        verbose_name_plural = _('Route Rule Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            RouteRuleData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = RouteRuleData.objects.get(id=self.id)
                self.pk = p.pk
            except RouteRuleData.DoesNotExist:
                pass

        super(RouteRuleData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.RouteRule.filter(Enabled=True):
            if v.Porduct.Name in res.keys():
                res[v.Porduct.Name].append(v.json())
            else:
                res[v.Porduct.Name] = [
                    v.json()
                ]
        return {
            "Version": self.__str__(),
            "ProductRule": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'route_rule.data'), 'w')as file:
            file.write(json.dumps(self.json()))
