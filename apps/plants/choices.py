from django.db import models


class PeriodResolutionChoices(models.TextChoices):
    SECOND = "PT1S", "Seconds"
    MINUTE = "PT1M", "Minutes"
    HOUR = "PT60M", "Hours"
    DAY = "P1D", "Days"
