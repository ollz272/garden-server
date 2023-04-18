from django.db import models


class WeatherTypes(models.IntegerChoices):
    """Different weather types we can have in the database."""

    "TODO, make these more precise!"
    CLEAR_SKY = 0, "Clear sky"

    MAINLY_CLEAR_1 = 1, "Mainly clear, partly cloudy, and overcast"
    MAINLY_CLEAR_2 = 2, "Mainly clear, partly cloudy, and overcast"
    MAINLY_CLEAR_3 = 3, "Mainly clear, partly cloudy, and overcast"

    FOG_1 = 45, "Fog and depositing rime fog"
    FOG_2 = 48, "Fog and depositing rime fog"

    DRIZZLE_1 = 51, "Drizzle: Light, moderate, and dense intensity"
    DRIZZLE_2 = 53, "Drizzle: Light, moderate, and dense intensity"
    DRIZZLE_3 = 55, "Drizzle: Light, moderate, and dense intensity"

    FREEZING_DRIZZLE_1 = 56, "Freezing Drizzle: Light and dense intensity"
    FREEZING_DRIZZLE_2 = 57, "Freezing Drizzle: Light and dense intensity"

    RAIN_1 = 61, "Rain: Slight, moderate and heavy intensity"
    RAIN_2 = 63, "Rain: Slight, moderate and heavy intensity"
    RAIN_3 = 65, "Rain: Slight, moderate and heavy intensity"

    FREEZING_RAIN_1 = 66, "Freezing Rain: Light and heavy intensity"
    FREEZING_RAIN_2 = 67, "Freezing Rain: Light and heavy intensity"

    SNOW_FALL_1 = 71, "Snow fall: Slight, moderate, and heavy intensity"
    SNOW_FALL_2 = 73, "Snow fall: Slight, moderate, and heavy intensity"
    SNOW_FALL_3 = 75, "Snow fall: Slight, moderate, and heavy intensity"

    SNOW_GRAINS = 77, "Snow grains"

    RAIN_SHOWERS_1 = 80, "Rain showers: Slight, moderate, and violent"
    RAIN_SHOWERS_2 = 81, "Rain showers: Slight, moderate, and violent"
    RAIN_SHOWERS_3 = 82, "Rain showers: Slight, moderate, and violent"

    SNOW_SHOWERS_1 = 85, "Snow showers slight and heavy"
    SNOW_SHOWERS_2 = 86, "Snow showers slight and heavy"

    THUNDERSTORM = 95, "Thunderstorm: Slight or moderate"

    THUNDERSTORM_HAIL_1 = 96, "Thunderstorm with slight and heavy hail"
    THUNDERSTORM_HAIL_2 = 99, "Thunderstorm with slight and heavy hail"
