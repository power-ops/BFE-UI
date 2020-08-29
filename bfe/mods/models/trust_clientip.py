from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import json

# Create your models here.
class TrustClientIPQuerySet(models.QuerySet):
    pass


class TrustClientIPManager(models.Manager):
    def get_queryset(self):
        return TrustClientIPQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Source in res.keys():
                res[v.Source].append(v.json())
            else:
                res[v.Source] = [v.json()]
        return res


class TrustClientIP(models.Model):
    Source = models.CharField(_('CharField'), max_length=64)
    Begin = models.CharField(_('Begin'), max_length=64)
    End = models.CharField(_('End'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = TrustClientIPManager()

    def __str__(self):
        return self.Source + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    def json(self):
        return {
            "Begin": self.Begin,
            "End": self.End
        }

    class Meta:
        db_table = 'ModTrustClientIP'
        verbose_name = _('Mod TrustClientIP')
        verbose_name_plural = _('Mod TrustClientIP')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = TrustClientIP.objects.get(id=self.id)
                self.pk = p.pk
            except TrustClientIP.DoesNotExist:
                pass

        super(TrustClientIP, self).save(*args, **kwargs)


class TrustClientIPDataQuerySet(models.QuerySet):
    pass


class TrustClientIPDataManager(models.Manager):
    def get_queryset(self):
        return TrustClientIPDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class TrustClientIPData(models.Model):
    Version = models.CharField(_('Version'), max_length=64)
    Config = models.TextField(_('Config'))
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = TrustClientIPDataManager()

    class Meta:
        db_table = 'ModTrustClientIPData'
        verbose_name = _('Mod TrustClientIP Data')
        verbose_name_plural = _('Mod TrustClientIP Data')

    def save(self, *args, **kwargs):
        self.Config = json.dumps(TrustClientIP.objects.json())
        if not self.pk:
            try:
                p = TrustClientIPData.objects.get(id=self.id)
                self.pk = p.pk
            except TrustClientIPData.DoesNotExist:
                pass

        super(TrustClientIPData, self).save(*args, **kwargs)
