import logging

from django.core.management.base import BaseCommand

from alerts.models import Alert, AlertLog

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for scanning alerts in the system, and creating any logs needed."""

    def handle(self, *args, **options):
        alert_logs = []
        # TODO have a way of automatically resolving logs if condition is "unmet"
        for alert in Alert.objects.all().select_related("user", "plant", "sensor"):
            if alert.lower_threshold and alert.latest_data_point <= alert.latest_data_point.data:
                if alert.alert_logs.order_by("created").addressed is True:
                    logger.info(f"Condition met for alert {alert}")
                    alert_logs.append(AlertLog(user=alert.user, alert=alert))
            elif alert.lower_threshold and alert.latest_data_point >= alert.latest_data_point.data:
                if alert.alert_logs.order_by("created").addressed is True:
                    logger.info(f"Condition met for alert {alert}")
                    alert_logs.append(AlertLog(user=alert.user, alert=alert))

        AlertLog.objects.bulk_create(alert_logs)
