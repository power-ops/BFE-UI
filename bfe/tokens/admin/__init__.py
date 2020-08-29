from django.contrib import admin
from tokens.models.token import Token
from tokens.admin.token import TokenAdmin

admin.site.register(Token, TokenAdmin)
