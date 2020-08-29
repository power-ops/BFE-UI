from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import json
import os


class VipRuleQuerySet(models.QuerySet):
    pass


class VipRuleManager(models.Manager):
    def get_queryset(self):
        return VipRuleQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Product2Vip in res.keys():
                # warn
                res[v.Product2Vip].append(v.json())
            else:
                res[v.Product2Vip] = [v.json()]
        return res


class VipRule(models.Model):
    Product2Vip = models.CharField(_('Product2Vip'), max_length=64)
    VipList = models.TextField(_('VipList'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = VipRuleManager()

    def __str__(self):
        return self.Product2Vip + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        return [x.strip() for x in self.VipList.split('\r') if x.strip()]

    class Meta:
        db_table = 'VipRule'
        verbose_name = _('Vip Rule')
        verbose_name_plural = _('Vip Rule')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = VipRule.objects.get(id=self.id)
                self.pk = p.pk
            except VipRule.DoesNotExist:
                pass

        super(VipRule, self).save(*args, **kwargs)


class VipRuleDataQuerySet(models.QuerySet):
    pass


class VipRuleDataManager(models.Manager):
    def get_queryset(self):
        return VipRuleDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            s = {
                "Version": "nil",
                "Vips": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'vip_rule.data'), 'w')as file:
            file.write(json.dumps(s))


class VipRuleData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Vips = models.ManyToManyField(VipRule, verbose_name=_('Vips'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = VipRuleDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'VipRuleData'
        verbose_name = _('Vip Rule Data')
        verbose_name_plural = _('Vip Rule Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            VipRuleData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = VipRuleData.objects.get(id=self.id)
                self.pk = p.pk
            except VipRuleData.DoesNotExist:
                pass
        super(VipRuleData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.Vips.filter(Enabled=True):
            if v.Product2Vip in res.keys():
                # warn
                res[v.Product2Vip].append(v.json())
            else:
                res[v.Product2Vip] = [v.json()]
        return {
            "Version": self.__str__(),
            "Vips": res,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'vip_rule.data'), 'w')as file:
            file.write(json.dumps(self.json()))
