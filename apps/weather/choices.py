from django.db import models


class WeatherTypes(models.IntegerChoices):
    """Different weather types we can have in the database."""

    CLEAR_SKY = 0, "Clear sky"

    MAINLY_CLEAR_1 = 1, "Mainly clear"
    MAINLY_CLEAR_2 = 2, "Mainly partly cloudy"
    MAINLY_CLEAR_3 = 3, "Mainly overcast"

    FOG_1 = 45, "Fog"
    FOG_2 = 48, "Depositing rime fog"

    DRIZZLE_1 = 51, "Light Drizzle"
    DRIZZLE_2 = 53, "Moderate Drizzle"
    DRIZZLE_3 = 55, "Heavy Drizzle"

    FREEZING_DRIZZLE_1 = 56, "Light Freezing Drizzle"
    FREEZING_DRIZZLE_2 = 57, "Heavy Freezing Drizzle"

    RAIN_1 = 61, "Slight Rain"
    RAIN_2 = 63, "Moderate Rain"
    RAIN_3 = 65, "Heavy Rain"

    FREEZING_RAIN_1 = 66, "Light Freezing Rain"
    FREEZING_RAIN_2 = 67, "Heavy Freezing Rain"

    SNOW_FALL_1 = 71, "Light Snow fall"
    SNOW_FALL_2 = 73, "Moderate Snow fall"
    SNOW_FALL_3 = 75, "Heavy Snow fall"

    SNOW_GRAINS = 77, "Snow grains"

    RAIN_SHOWERS_1 = 80, "Slight Rain showers"
    RAIN_SHOWERS_2 = 81, "Moderate Rain showers"
    RAIN_SHOWERS_3 = 82, "Heavy Rain showers"

    SNOW_SHOWERS_1 = 85, "Slight Snow showers"
    SNOW_SHOWERS_2 = 86, "Heavy Snow showers"

    THUNDERSTORM = 95, "Thunderstorm"

    THUNDERSTORM_HAIL_1 = 96, "Thunderstorm with slight hail"
    THUNDERSTORM_HAIL_2 = 99, "Thunderstorm with heavy hail"
