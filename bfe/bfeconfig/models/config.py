from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import server_data_conf.models as server_data_conf
import cluster_conf.models as cluster_conf
import tls_conf.models as tls_conf
from django.conf import settings
import uuid
import os
import zipfile


# Create your models here.
class BfeConfigQuerySet(models.QuerySet):
    pass


class BfeConfigManager(models.Manager):
    def get_queryset(self):
        return BfeConfigQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def get_by_appname(self, Name):
        return self.get_queryset().filter(Name=Name).all()


class BfeConfig(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    UUID = models.UUIDField(_('UUID'), default=uuid.uuid4)
    ZipFile = models.BinaryField(_('ZipFile'))
    # Enabled = models.BooleanField(default=True)
    # server_data_conf
    ClusterConfig = models.ForeignKey(server_data_conf.ClusterConfigData, verbose_name=_("ClusterConfigData"),
                                      on_delete=models.CASCADE)
    HostRule = models.ForeignKey(server_data_conf.HostRuleData, verbose_name=_("HostRuleData"),
                                 on_delete=models.CASCADE)
    NameConfig = models.ForeignKey(server_data_conf.NameConfigData, verbose_name=_("NameConfigData"),
                                   on_delete=models.CASCADE)
    RouteRule = models.ForeignKey(server_data_conf.RouteRuleData, verbose_name=_("RouteRuleData"),
                                  on_delete=models.CASCADE)
    VipRule = models.ForeignKey(server_data_conf.VipRuleData, verbose_name=_("VipRuleData"),
                                on_delete=models.CASCADE)
    # cluster_conf
    ClusterTable = models.ForeignKey(cluster_conf.ClusterTableData, verbose_name=_("ClusterTableData"),
                                     on_delete=models.CASCADE)
    GSLB = models.ForeignKey(cluster_conf.GSLBData, verbose_name=_("GSLB Data"), on_delete=models.CASCADE)

    # tls_conf
    ServerCertConf = models.ForeignKey(tls_conf.CertData, verbose_name=_("Cert Data"), on_delete=models.CASCADE)
    SessionTicketKey = models.ForeignKey(tls_conf.SessionTicketKey, verbose_name=_("Session Ticket Key"),
                                         on_delete=models.CASCADE)
    TLSRuleConf = models.ForeignKey(tls_conf.TLSRuleData, verbose_name=_("TLS Rule Data"), on_delete=models.CASCADE)

    # mod

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)
    objects = BfeConfigManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    class Meta:
        db_table = 'BfeConfig'
        verbose_name = _('Bfe Config')
        verbose_name_plural = _('Bfe Config')

    def save(self, *args, **kwargs):
        if self.Enabled:
            BfeConfig.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
            self.ClusterConfig.tofile()
            # server_data_conf
            self.HostRule.tofile()
            self.NameConfig.tofile()
            self.RouteRule.tofile()
            self.VipRule.tofile()

            # cluster_conf
            self.ClusterTable.tofile()
            self.GSLB.tofile()

            # tls_conf
            self.ServerCertConf.tofile()
            self.SessionTicketKey.tofile()
            self.TLSRuleConf.tofile()

            # mod
            f = zipfile.ZipFile(str(self.UUID) + '.zip', 'w', zipfile.ZIP_DEFLATED)
            startdir = os.path.join(settings.BASE_DIR, 'conf')
            for dirpath, dirnames, filenames in os.walk(startdir):
                for filename in filenames:
                    f.write(os.path.join(dirpath, filename), os.path.join(dirpath.replace(startdir, '', 1), filename))
            f.close()
            self.ZipFile = open(str(self.UUID) + '.zip', 'rb').read()

        if not self.pk:
            try:
                p = BfeConfig.objects.get(id=self.id)
                self.pk = p.pk
            except BfeConfig.DoesNotExist:
                pass
        super(BfeConfig, self).save(*args, **kwargs)
