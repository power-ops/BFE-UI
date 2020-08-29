from django.contrib import admin
from product.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _


class ProductForm(forms.ModelForm):
    Name = forms.CharField(label=_('Name'), max_length=64)
    Comment = forms.CharField(label=_('Comment'), widget=forms.Textarea)
    Enabled = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = Product
        exclude = ['CreateDate']
        fields = ['Name', 'Comment', 'Enabled']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Comment', 'Enabled', 'CreateDate')
    form = ProductForm
    list_filter = ('Name',)
    list_per_page = 20
    search_fields = ['Name']


admin.site.register(Product, ProductAdmin)
