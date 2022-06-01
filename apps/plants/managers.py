from django.db import models


class PlantDataManager(models.QuerySet):
    def to_chart_data(self):
        plants = set(self.values_list("plant", "plant__name"))

        chart_data = {}
        for plant_id, plant_name in plants:
            qs = self.filter(plant=plant_id)
            data = {
                "times": [date.strftime("%m/%d/%Y, %H:%M:%S") for date in qs.values_list("time", flat=True)],
                "temperatures": list(qs.values_list("temperature", flat=True)),
                "light_levels": list(qs.values_list("light_level", flat=True)),
                "moisture_level": list(qs.values_list("moisture_level", flat=True)),
            }
            chart_data[plant_name] = data

        return chart_data
