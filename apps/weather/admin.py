from django.contrib import admin

from .models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_filter = ["date_time", "location", "is_forecast", "weather_code"]
    readonly_fields = ["is_forecast", "created", "updated"]
    list_display = ["date_time", "location", "is_forecast", "weather_code"]

    fieldsets = [
        (
            "Weather Info",
            {
                "fields": ["date_time", "location"],
            },
        ),
        ("Weather Data", {"fields": ["temperature", "apparent_temperature", "rain", "cloud_cover", "weather_code"]}),
        (
            "Meta Data",
            {
                "classes": ["collapse"],
                "fields": ["is_forecast", "created", "updated"],
            },
        ),
    ]
