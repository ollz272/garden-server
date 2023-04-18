from django.contrib import admin

from .models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_filter = ["date_time", "location", "is_forecast"]
    read_only_fields = ["is_forecast", "created", "updated"]
