from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db import models as gis_models


class Zone(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    location = gis_models.PointField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="unique_zone_name_for_user")]
        indexes = [models.Index(fields=["location"], name="zone_location_idx")]
