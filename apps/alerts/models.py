from functools import cached_property

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Alert(models.Model):
    """An alert for a user.

    An alert is a configurable model that users can create to get notified about changes to their plants.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="alerts")
    plant = models.ForeignKey("plants.Plant", on_delete=models.CASCADE, related_name="alerts")
    sensor = models.ForeignKey("plants.Sensor", on_delete=models.CASCADE, related_name="alerts")

    name = models.CharField(max_length=128)

    upper_threshold = models.FloatField(blank=True, null=True)
    lower_threshold = models.FloatField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @cached_property
    def latest_data_point(self):
        return self.sensor.plant_data.order_by("time").first()

    def __str__(self):
        return self.name


class AlertLog(models.Model):
    """An alert log from an alert.

    Created when the conditions of an alert are met.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="alert_logs")
    addressed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
