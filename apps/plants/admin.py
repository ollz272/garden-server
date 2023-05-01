from django.contrib import admin

from .models import DataPoint, Plant, SensorUnit


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


@admin.register(DataPoint)
class PlantDataPointAdmin(admin.ModelAdmin):
    list_filter = ("plant",)
    list_select_related = ("plant",)


@admin.register(SensorUnit)
class SensorUnitAdmin(admin.ModelAdmin):
    fields = ("name",)
