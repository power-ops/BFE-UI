from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from product.models import Product
from django.conf import settings
import json
import os


class HostTagQuerySet(models.QuerySet):
    pass


class HostTagManager(models.Manager):
    def get_queryset(self):
        return HostTagQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Tag in res.keys():
                res[v.Tag].append(v.json())
            else:
                res[v.Tag] = [v.json()]
        return res


class HostTag(models.Model):
    Tag = models.CharField(_('Tag'), max_length=64)
    Domain = models.CharField(_('Domain'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = HostTagManager()

    def __str__(self):
        return self.Tag + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return self.Domain

    class Meta:
        db_table = 'HostTag'
        verbose_name = _('Host Tag')
        verbose_name_plural = _('Host Tag')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = HostTag.objects.get(id=self.id)
                self.pk = p.pk
            except HostTag.DoesNotExist:
                pass

        super(HostTag, self).save(*args, **kwargs)


class HostProductQuerySet(models.QuerySet):
    pass


class HostProductManager(models.Manager):
    def get_queryset(self):
        return HostProductQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Product.Name in res.keys():
                res[v.Product.Name].append(v.json())
            else:
                res[v.Product.Name] = [v.json()]
        return res


class HostProduct(models.Model):
    Product = models.OneToOneField(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    Tag = models.OneToOneField(HostTag, verbose_name=_('Tag'), on_delete=models.CASCADE)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = HostProductManager()

    def __str__(self):
        return self.Product.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return self.Tag.Tag

    class Meta:
        db_table = 'HostProduct'
        verbose_name = _('Host Product')
        verbose_name_plural = _('Host Product')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = HostProduct.objects.get(id=self.id)
                self.pk = p.pk
            except HostProduct.DoesNotExist:
                pass

        super(HostProduct, self).save(*args, **kwargs)


class HostRuleDataQuerySet(models.QuerySet):
    pass


class HostRuleDataManager(models.Manager):
    def get_queryset(self):
        return HostRuleDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            s = {
                "Version": "nil",
                "DefaultProduct": None,
                "HostTags": {},
                "Hosts": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'host_rule.data'), 'w')as file:
            file.write(json.dumps(s))


class HostRuleData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    DefaultProduct = models.CharField(_('Default Product'), max_length=64, default=None)

    Hosts = models.ManyToManyField(HostProduct, verbose_name=_('Hosts'), default=None)
    HostTags = models.ManyToManyField(HostTag, verbose_name=_('HostTags'), default=None)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = HostRuleDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'HostRuleData'
        verbose_name = _('Host Rule Data')
        verbose_name_plural = _('Host Rule Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            HostRuleData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = HostRuleData.objects.get(id=self.id)
                self.pk = p.pk
            except HostRuleData.DoesNotExist:
                pass

        super(HostRuleData, self).save(*args, **kwargs)

    def json(self):
        Hosts = {}
        HostTags = {}
        for v in self.Hosts.filter(Enabled=True):
            if v.Product in HostTags.keys():
                HostTags[v.Product.Name].append(v.json())
            else:
                HostTags[v.Product.Name] = [v.json()]
        for v in self.HostTags.filter(Enabled=True):
            if v.Tag in Hosts.keys():
                Hosts[v.Tag].append(v.json())
            else:
                Hosts[v.Tag] = [v.json()]
        return {
            "Version": self.__str__(),
            "DefaultProduct": None if self.DefaultProduct == "" else self.DefaultProduct,
            "HostTags": HostTags,
            "Hosts": Hosts,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'server_data_conf', 'host_rule.data'), 'w')as file:
            file.write(json.dumps(self.json()))
