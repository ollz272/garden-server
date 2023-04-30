import logging

from alerts.models import Alert, AlertLog
from django.core.management.base import BaseCommand

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for scanning alerts in the system, and creating any logs needed."""

    def handle(self, *args, **options):
        alert_logs = []
        # TODO have a way of automatically resolving logs if condition is "unmet"
        for alert in Alert.objects.all().select_related("user", "plant", "sensor"):
            self.stdout.write(f"Checking condition on {alert}")
            if alert.lower_threshold and alert.latest_data_point.data <= alert.lower_threshold:
                latest_log = alert.alert_logs.order_by("-created").first()
                if not latest_log or latest_log.addressed:
                    self.stdout.write(f"Condition met for alert {alert}")
                    alert_logs.append(AlertLog(user=alert.user, alert=alert))
            elif alert.upper_threshold and alert.latest_data_point.data >= alert.upper_threshold:
                latest_log = alert.alert_logs.order_by("-created").first()
                if not latest_log or latest_log.addressed:
                    self.stdout.write(f"Condition met for alert {alert}")
                    alert_logs.append(AlertLog(user=alert.user, alert=alert))
            else:
                self.stdout.write(f"No conditions met for {alert}")

        AlertLog.objects.bulk_create(alert_logs)
