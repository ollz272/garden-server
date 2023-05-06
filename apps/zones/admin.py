from django.contrib import admin
from zones.models import Zone


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    pass
