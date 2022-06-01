from django.db import models
from django.utils.text import slugify

from .managers import PlantDataManager


class Plant(models.Model):
    # TODO.
    name = models.CharField(max_length=256)
    indoor = models.BooleanField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super(Plant, self).save(*args, **kwargs)


class DataPoint(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="plant_data")
    time = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True)
    light_level = models.FloatField(null=True)
    moisture_level = models.FloatField(null=True)

    objects = PlantDataManager.as_manager()

    class Meta:
        ordering = ("-time",)

    @property
    def to_structured_data(self):
        return {
            "time": self.time,
            "temperature": self.temperature,
            "light_level": self.light_level,
            "moisture_level": self.moisture_level,
        }
