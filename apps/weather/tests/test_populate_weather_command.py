from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class TestPopulateWeatherCommand(TestCase):
    @patch("weather.management.commands.populate_weather.Command.get_weather_data")
    def do_command(self, func, return_value):
        """Helper function for mocking the response to an api call."""
        func.return_value = return_value

        call_command("populate_weather")

    # TODO.
