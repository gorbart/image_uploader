import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from image_handler.models import Image

logger = logging.getLogger(__name__)


def delete_expired_images():
    images = Image.objects.filter(expiry_time__lt=timezone.now())

    for image in images:
        image.delete()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_expired_images,
            trigger=CronTrigger(second="*/1"),  # Every 10 seconds
            id="delete_expired_images",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'delete_expired_images'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")