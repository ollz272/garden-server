from django.contrib import admin

from alerts.models import Alert


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
