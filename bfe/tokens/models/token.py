from django.db import models
import uuid
import bfeconfig.models as bfeconfig
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class TokenQuerySet(models.QuerySet):
    pass


class TokenManager(models.Manager):
    def get_queryset(self):
        return TokenQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def get_by_appname(self, AppName):
        return self.get_queryset().filter(AppName=AppName).all()


# Create your models here.
class Token(models.Model):
    AppName = models.CharField(_('AppName'), max_length=64)
    TokenId = models.UUIDField(_('TokenId'), default=uuid.uuid4)
    BfeConfig = models.ForeignKey(bfeconfig.BfeConfig, verbose_name=_("BfeConfig"),
                                  on_delete=models.CASCADE)
    Comment = models.TextField(_('Comment'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = TokenManager()

    def __str__(self):
        return self.AppName

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    class Meta:
        db_table = 'Token'
        verbose_name = _('Token')
        verbose_name_plural = _('Token')

    def save(self, *args, **kwargs):
        if self.Enabled:
            Token.objects.filter(AppName=self.AppName, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = Token.objects.get(id=self.id)
                self.pk = p.pk
            except Token.DoesNotExist:
                pass

        super(Token, self).save(*args, **kwargs)
