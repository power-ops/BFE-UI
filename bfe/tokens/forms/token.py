from tokens.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _


class TokenForm(forms.ModelForm):
    AppName = forms.CharField(label=_('AppName'), max_length=64)

    class Meta:
        model = Token
        exclude = ['CreateDate']

    def save(self, commit=True):
        instance = super(TokenForm, self).save(commit=False)
        if len(self.changed_data) > 0 and len(
                Token.objects.get_by_appname(AppName=self.instance.AppName)) > 0 and self.instance.Enabled:
            if self.instance.id:
                Token.objects.create(AppName=self.instance.AppName,
                                     TokenId=self.instance.TokenId,
                                     BfeConfig=self.instance.BfeConfig,
                                     Comment=self.instance.Comment,
                                     Enabled=True,
                                     ).save()
                instance.BfeConfig = Token.objects.get_by_id(self.instance.id).BfeConfig
                instance.Comment = Token.objects.get_by_id(self.instance.id).Comment
                instance.Enabled = False
            else:
                instance.TokenId = Token.objects.get_by_appname(AppName=self.instance.AppName)[0].TokenId
        return instance
