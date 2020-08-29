from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import json
import os


class SessionTicketKeyQuerySet(models.QuerySet):
    pass


class SessionTicketKeyManager(models.Manager):
    def get_queryset(self):
        return SessionTicketKeyQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def tofile(self, id):
        data = self.get_queryset().filter(id=id).first()
        if data:
            s = data.json()
        else:
            s = {
                "Version": "nil",
                "SessionTicketKey": "",
            }
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'session_ticket_key.data'), 'w')as file:
            file.write(json.dumps(s))


class SessionTicketKey(models.Model):
    Name = models.CharField(_('Name'), max_length=64)
    SessionTicketKey = models.TextField(_('SessionTicketKey'))

    Enabled = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = SessionTicketKeyManager()

    def __str__(self):
        if self.Enabled:
            return self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "!!!Disabled_" + self.Name + "_" + self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'SessionTicketKey'
        verbose_name = _('Session Ticket Key')
        verbose_name_plural = _('Session Ticket Key')

    def save(self, *args, **kwargs):
        if self.Enabled:
            SessionTicketKey.objects.filter(Name=self.Name, Enabled=True).update(Enabled=False)
        if not self.pk:
            try:
                p = SessionTicketKey.objects.get(id=self.id)
                self.pk = p.pk
            except SessionTicketKey.DoesNotExist:
                pass
        super(SessionTicketKey, self).save(*args, **kwargs)

    def json(self):
        return {
            "Version": self.__str__(),
            "SessionTicketKey": self.SessionTicketKey,
        }

    def tofile(self):
        with open(os.path.join(settings.BASE_DIR, 'conf', 'tls_conf', 'session_ticket_key.data'), 'w')as file:
            file.write(json.dumps(self.json()))
