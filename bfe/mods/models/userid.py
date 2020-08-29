from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from product.models import Product
import json
from django.conf import settings
import os


# Create your models here.
class UserIdQuerySet(models.QuerySet):
    pass


class UserIdManager(models.Manager):
    def get_queryset(self):
        return UserIdQuerySet(self.model, using=self._db)

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


class UserId(models.Model):
    Porduct = models.ForeignKey(Product, verbose_name=_('Porduct'), on_delete=models.CASCADE)
    Cond = models.CharField(_('Cond'), max_length=64)
    ParamsName = models.CharField(_('ParamsName'), max_length=64)
    ParamsDomain = models.CharField(_('ParamsDomain'), max_length=64)
    ParamsPath = models.CharField(_('ParamsPath'), max_length=64)
    ParamsMaxAge = models.IntegerField(_('ParamsMaxAge'))
    Generator = models.CharField(_('Generator'), max_length=64)

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = UserIdManager()

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
            "Params": {
                "Name": self.ParamsName,
                "Domain": self.ParamsDomain,
                "Path": self.ParamsPath,
                "MaxAge": self.ParamsMaxAge
            },
            "Generator": self.Generator
        }

    class Meta:
        db_table = 'ModUserId'
        verbose_name = _('Mod UserId')
        verbose_name_plural = _('Mod UserId')

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserId.objects.get(id=self.id)
                self.pk = p.pk
            except UserId.DoesNotExist:
                pass

        super(UserId, self).save(*args, **kwargs)


class UserIdDataQuerySet(models.QuerySet):
    pass


class UserIdDataManager(models.Manager):
    def get_queryset(self):
        return UserIdDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class UserIdData(models.Model):
    Version = models.CharField(_('Version'), max_length=64)
    Products = models.TextField(_('Products'))
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = UserIdDataManager()

    def __str__(self):
        return self.Version + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'ModUserIdData'
        verbose_name = _('Mod UserId Data')
        verbose_name_plural = _('Mod UserId Data')

    def save(self, *args, **kwargs):
        self.Products = json.dumps(UserId.objects.json())
        if not self.pk:
            try:
                p = UserIdData.objects.get(id=self.id)
                self.pk = p.pk
            except UserIdData.DoesNotExist:
                pass

        super(UserIdData, self).save(*args, **kwargs)
        with open(os.path.join(settings.BASE_DIR, 'conf', 'mod_userid', 'userid_rule.data'), 'w')as file:
            file.write(json.dumps({
                "Version": self.__str__(),
                "Products": json.loads(self.Products),
            }))
