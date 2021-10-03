from django.contrib import admin

from djangogramm.models import DgUser, DgPost

# Register your models here.

admin.site.register(DgUser)
admin.site.register(DgPost)