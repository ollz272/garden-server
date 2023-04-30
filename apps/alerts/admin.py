from alerts.models import Alert, AlertLog
from django.contrib import admin

# Register your models here.


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_filter = ["user", "plant", "sensor"]
    readonly_fields = ["created", "updated"]
    list_display = ["name", "user", "plant", "sensor"]

    fieldsets = [
        (
            "Alert Info",
            {
                "fields": ["user", "plant", "sensor", "name", "upper_threshold", "lower_threshold"],
            },
        ),
        (
            "Meta Data",
            {
                "classes": ["collapse"],
                "fields": ["created", "updated"],
            },
        ),
    ]


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_filter = ["user", "addressed"]
    readonly_fields = ["created", "updated"]
    list_display = ["alert", "created", "updated", "addressed"]

    fieldsets = [
        (
            "Alert Log Info",
            {
                "fields": ["user", "alert", "addressed"],
            },
        ),
        (
            "Meta Data",
            {
                "classes": ["collapse"],
                "fields": ["created", "updated"],
            },
        ),
    ]
