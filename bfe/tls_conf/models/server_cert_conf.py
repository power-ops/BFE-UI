from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import shutil
from django.conf import settings
import json
import os


class CertQuerySet(models.QuerySet):
    pass


class CertManager(models.Manager):
    def get_queryset(self):
        return CertQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self):
        for v in self.get_queryset().filter(Enabled=True):
            with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'certs', v.ServerCertName), 'w')as file:
                file.write(v.ServerCertData.decode('utf-8'))
            with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'certs', v.ServerKeyName), 'w')as file:
                file.write(v.ServerKeyData.decode('utf-8'))

    def json(self):
        res = {}
        for v in self.get_queryset().filter(Enabled=True):
            if v.Domain in res.keys():
                # warn
                res[v.Domain] = v.json()
            else:
                res[v.Domain] = v.json()
        return res


class Cert(models.Model):
    Domain = models.CharField(_('Domain'), max_length=64)
    ServerKeyData = models.BinaryField(verbose_name=_('ServerKey'))
    ServerKeyName = models.CharField(_('ServerKeyName'), max_length=64, default='')
    ServerCertData = models.BinaryField(verbose_name=_('ServerCert'))
    ServerCertName = models.CharField(_('ServerCertName'), max_length=64, default='')

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = CertManager()

    def __str__(self):
        if self.Enabled:
            return self.Domain + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Domain + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        return {
            "ServerCertFile": "tls_conf/certs/" + self.ServerCertName,
            "ServerKeyFile": "tls_conf/certs/" + self.ServerKeyName,
        }

    class Meta:
        db_table = 'Cert'
        verbose_name = _('Cert')
        verbose_name_plural = _('Cert')

    def save(self, *args, **kwargs):
        if self.Enabled:
            Cert.objects.filter(Domain=self.Domain, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = Cert.objects.get(id=self.id)
                self.pk = p.pk
            except Cert.DoesNotExist:
                pass

        super(Cert, self).save(*args, **kwargs)


class CertDataQuerySet(models.QuerySet):
    pass


class CertDataManager(models.Manager):
    def get_queryset(self):
        return CertDataQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            # TODO: try config is nil
            s = {
                "Version": "nil",
                "Config": {},
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'server_cert_conf.data'), 'w')as file:
            file.write(json.dumps(s))


class CertData(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    Default = models.CharField(_('Default'), max_length=64)
    CertConf = models.ManyToManyField(Cert, verbose_name=_('CertConf'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = CertDataManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'CertData'
        verbose_name = _('Cert Data')
        verbose_name_plural = _('Cert Data')

    def save(self, *args, **kwargs):
        if self.Enabled:
            CertData.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = CertData.objects.get(id=self.id)
                self.pk = p.pk
            except CertData.DoesNotExist:
                pass
        super(CertData, self).save(*args, **kwargs)

    def json(self):
        res = {}
        for v in self.CertConf.filter(Enabled=True):
            if v.Domain in res.keys():
                # warn
                res[v.Domain] = v.json()
            else:
                res[v.Domain] = v.json()
        return {
            "Version": self.__str__(),
            "Config": {
                "Default": self.Default,
                "CertConf": res
            },
        }

    def tofile(self):
        shutil.rmtree(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'certs'), ignore_errors=True)
        os.mkdir(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'certs'))
        Cert.objects.tofile()
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'server_cert_conf.data'), 'w')as file:
            file.write(json.dumps(self.json()))
