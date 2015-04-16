from django.contrib import admin
from django import forms
from django.db import models

from models import Article, Navigation


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class': 'ckeditor'})}}
    list_display = ('slug', 'get_url')

    class Media:
        js = ('/static/js/ckeditor/ckeditor.js',)


class NavigationAdmin(admin.ModelAdmin):
    list_display = ('text', 'parent', 'order', 'article')
    ordering = ('order',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Navigation, NavigationAdmin)
