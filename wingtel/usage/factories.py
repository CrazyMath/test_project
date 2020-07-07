import datetime
import random

import factory

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.att_subscriptions.factories import ATTSubscriptionFactory
from wingtel.usage.models import DataUsageRecord, VoiceUsageRecord


class DataUsageRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DataUsageRecord

    @factory.lazy_attribute
    def att_subscription_id(self):
        if not ATTSubscription.objects.all().exists():
            ATTSubscriptionFactory.create_batch(5)
        att_subscriptions = ATTSubscription.objects.all()
        return random.choice(att_subscriptions)

    price = random.randint(1, 100)
    usage_date = factory.LazyFunction(datetime.datetime.now)
    kilobytes_used = random.randint(1, 100)


class VoiceUsageRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VoiceUsageRecord

    @factory.lazy_attribute
    def att_subscription_id(self):
        if not ATTSubscription.objects.all().exists():
            ATTSubscriptionFactory.create_batch(5)
        att_subscriptions = ATTSubscription.objects.all()
        return random.choice(att_subscriptions)

    price = random.randint(1, 100)
    usage_date = factory.LazyFunction(datetime.datetime.now)
    seconds_used = random.randint(1, 100)
