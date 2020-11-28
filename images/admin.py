from django.contrib import admin

# Register your models here.
from .models import TemplateStore, Template


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'processed', ]


admin.site.register(TemplateStore)
admin.site.register(Template, TemplateAdmin)
