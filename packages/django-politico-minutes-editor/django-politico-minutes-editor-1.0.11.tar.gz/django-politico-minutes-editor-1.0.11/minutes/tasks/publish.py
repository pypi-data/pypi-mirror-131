import logging

from celery import shared_task
from django.conf import settings
from minutes.models import Edition
from minutes.api.common.serializers.edition import EditionLiveSerializer
from minutes.utils.aws_lambda import invoke
from minutes.utils.aws_s3 import put_json


headers = {
    "Authorization": "Token {}".format(settings.MINUTES_API_TOKEN),
    "Content-Type": "application/json",
}

logger = logging.getLogger("django")


@shared_task(acks_late=True)
def publish(epk, mode="STAGING"):
    edition = Edition.objects.get(id=epk)
    vertical = edition.vertical.slug

    data = {
      "body": {
        "manual": True,
        "testing": settings.DEBUG,
        "token": settings.MINUTES_BAKERY_TOKEN,
        "mode": mode,
        "verticalSlug": vertical,
        "editionId": str(edition.id)
      }
    }

    resp = invoke(data)

    if mode == "PRODUCTION" and resp.ok:
        edition.is_published = True
        edition.save()
        publish_api_if_latest(epk, mode)

    return resp


@shared_task(acks_late=True)
def publish_api_if_latest(epk, mode="STAGING"):
    edition = Edition.objects.get(id=epk)

    publish_pah = "interactives/databases/minutes/{}/{}/{}".format(
        edition.vertical.slug,
        "latest-live",
        "data.json"
    )

    if edition.is_latest_live():
        data = EditionLiveSerializer(edition).data
        return put_json(data, publish_pah, mode=mode)


@shared_task(acks_late=True)
def unpublish(edition):
    pass
    # data = {"action": "unpublish", "data": edition}
    #
    # e = Edition.objects.get(id=edition)
    # e.live = False
    # e.save()
    #
    # if e == Edition.objects.latest_live(e.vertical):
    #     publish_latest(e.vertical.id.hex)
    #
    # requests.post(settings.MINUTES_BAKERY_URL, json=data, headers=headers)


@shared_task(acks_late=True)
def publish_latest(vertical):
    # change this to PRODUCTION when launching
    e = Edition.objects.latest_live(vertical)
    return publish(str(e.id), "PRODUCTION")


@shared_task(acks_late=True)
def publish_if_ready(edition):
    e = Edition.objects.get(id=edition)
    if e.should_publish():
        # change this to PRODUCTION when launching
        return publish(edition, "PRODUCTION")


@shared_task(acks_late=True)
def autopublisher():
    logger.info("MINUTES: Starting autopublishing cycle...")
    for e in Edition.objects.all():
        if not e.is_published and e.should_publish():
            logger.info('MINUTES: Publishing edition "{}"...'.format(
                e.id
            ))
            publish(e.id, "PRODUCTION")

    logger.info("MINUTES: Autopublishing cycle complete.")
