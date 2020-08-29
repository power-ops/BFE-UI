from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from product.models import Product
import json

# Create your models here.
class BlockQuerySet(models.QuerySet):
    pass


class BlockManager(models.Manager):
    def get_queryset(self):
        return BlockQuerySet(self.model, using=self._db)

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


class Block(models.Model):
    Porduct = models.ForeignKey(Product, verbose_name=_('Porduct'), on_delete=models.CASCADE)
    action_cmd = models.CharField(_('action_cmd'), max_length=64)
    action_params = models.CharField(_('action_params'), max_length=64)
    name = models.CharField(_('name'), max_length=64)
    cond = models.CharField(_('cond'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = BlockManager()

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
            "cond": self.cond,
            "name": self.name,
            "action": {
                "cmd": self.action_cmd,
                "params": self.action_params,
            },
        }

    class Meta:
        db_table = 'ModBlock'
        verbose_name = _('Mod Block')
        verbose_name_plural = _('Mod Block')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Block.objects.get(id=self.id)
                self.pk = p.pk
            except Block.DoesNotExist:
                pass
        super(Block, self).save(*args, **kwargs)


class BlockDataQuerySet(models.QuerySet):
    pass


class BlockDataManager(models.Manager):
    def get_queryset(self):
        return BlockDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class BlockData(models.Model):
    Version = models.CharField(_('Version'), max_length=64)
    Config = models.TextField(_('Config'))
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = BlockDataManager()

    class Meta:
        db_table = 'ModBlockData'
        verbose_name = _('Mod Block Data')
        verbose_name_plural = _('Mod Block Data')

    def save(self, *args, **kwargs):
        self.Config = json.dumps(Block.objects.json())
        if not self.pk:
            try:
                p = BlockData.objects.get(id=self.id)
                self.pk = p.pk
            except BlockData.DoesNotExist:
                pass

        super(BlockData, self).save(*args, **kwargs)


class BlockIPBlacklistQuerySet(models.QuerySet):
    pass


class BlockIPBlacklistManager(models.Manager):
    def get_queryset(self):
        return BlockIPBlacklistQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class BlockIPBlacklist(models.Model):
    ip = models.CharField(_('ip'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = BlockIPBlacklistManager()

    def __str__(self):
        return self.ip + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    class Meta:
        db_table = 'ModBlockIPBlacklist'
        verbose_name = _('Mod Block IPBlacklist')
        verbose_name_plural = _('Mod Block IPBlacklist')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = BlockIPBlacklist.objects.get(id=self.id)
                self.pk = p.pk
            except BlockIPBlacklist.DoesNotExist:
                pass
        super(BlockIPBlacklist, self).save(*args, **kwargs)
