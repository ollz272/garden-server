from django.contrib import admin

from .models import DataPoint, Plant

# Register your models here.


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


@admin.register(DataPoint)
class PlantDataPointAdmin(admin.ModelAdmin):
    pass
