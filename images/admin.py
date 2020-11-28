from django.contrib import admin

# Register your models here.
from .models import TemplateStore, Template

admin.site.register(TemplateStore)
admin.site.register(Template)
