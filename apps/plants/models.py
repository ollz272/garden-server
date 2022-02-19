from django.db import models

# Create your models here.
from django.utils.text import slugify


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
