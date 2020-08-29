from django.contrib import admin
from bfeconfig.models import BfeConfig
from bfeconfig.admin.config import BfeConfigAdmin

admin.site.register(BfeConfig, BfeConfigAdmin)
