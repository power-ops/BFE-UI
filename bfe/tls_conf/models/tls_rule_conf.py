from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from product.models import Product
from django.conf import settings
import json
import os


class TLSRuleQuerySet(models.QuerySet):
    pass


class TLSRuleManager(models.Manager):
    def get_queryset(self):
        return TLSRuleQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Product.Name in res.keys():
                # warn
                res[v.Product.Name] = v.json()
            else:
                res[v.Product.Name] = v.json()
        return res


class TLSRule(models.Model):
    Product = models.OneToOneField(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    VipConf = models.TextField(_('VipConf'))
    SniConf = models.CharField(_('SniConf'), max_length=64, default=None)
    CertName = models.CharField(_('CertName'), max_length=64)
    NextProtos = models.TextField(_('NextProtos'))
    Grade = models.CharField(_('Grade'), max_length=64)
    ClientCAName = models.CharField(_('ClientCAName'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = TLSRuleManager()

    def __str__(self):
        return self.Product.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        return {
            "VipConf": [x.strip() for x in self.VipConf.split('\r') if x.strip()],
            "SniConf": None if self.SniConf == "" else self.SniConf,
            "CertName": self.CertName,
            "NextProtos": [x.strip() for x in self.NextProtos.split('\r') if x.strip()],
            "Grade": self.Grade,
            "ClientCAName": self.ClientCAName,
        }

    class Meta:
        db_table = 'TLSRule'
        verbose_name = _('TLS Rule')
        verbose_name_plural = _('TLS Rule')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = TLSRule.objects.get(id=self.id)
                self.pk = p.pk
            except TLSRule.DoesNotExist:
                pass

        super(TLSRule, self).save(*args, **kwargs)


class TLSRuleDataQuerySet(models.QuerySet):
    pass


class TLSRuleDataManager(models.Manager):
    def get_queryset(self):
        return TLSRuleDataQuerySet(self.model, using=self._db)

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
                "DefaultNextProtos": ["http/1.1"],
            }
        #     TODO: verify DefaultNextProtos empty value
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'tls_rule_conf.data'), 'w')as file:
            file.write(json.dumps(s))


class TLSRuleData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    DefaultNextProtos = models.TextField(_('DefaultNextProtos'))
    Config = models.ManyToManyField(TLSRule, verbose_name=_('Config'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = TLSRuleDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'TLSRuleData'
        verbose_name = _('TLS Rule Data')
        verbose_name_plural = _('TLS Rule Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            TLSRuleData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = TLSRuleData.objects.get(id=self.id)
                self.pk = p.pk
            except TLSRuleData.DoesNotExist:
                pass
        super(TLSRuleData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.Config.filter(Enabled=True):
            if v.Product.Name in res.keys():
                # warn
                res[v.Product.Name] = v.json()
            else:
                res[v.Product.Name] = v.json()
        return {
            "Version": self.__str__(),
            "Config": res,
            "DefaultNextProtos": [x.strip() for x in self.DefaultNextProtos.split('\r') if x.strip()],
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'tls_rule_conf.data'), 'w')as file:
            file.write(json.dumps(self.json()))
