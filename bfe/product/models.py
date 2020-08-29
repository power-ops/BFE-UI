from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class ProductQuerySet(models.QuerySet):
    pass


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class Product(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Comment = models.TextField(_('Comment'))
    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)
    objects = ProductManager()

    def __str__(self):
        return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'Product'
        verbose_name = _('Product')
        verbose_name_plural = _('Product')
