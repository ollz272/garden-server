from django.contrib import admin

from .models import DataPoint, Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    list_filter = ("indoor",)


@admin.register(DataPoint)
class PlantDataPointAdmin(admin.ModelAdmin):
    list_filter = ("plant",)
    list_select_related = ("plant",)
