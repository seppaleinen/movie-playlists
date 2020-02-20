from celery import shared_task
import logging
from importer import models

logger = logging.getLogger(__name__)


@shared_task
def build_something():
    for i in models.KeywordIds.objects.filter(pk=278).all():
        logger.info("Hej: %s" % i)
    return "hej"
