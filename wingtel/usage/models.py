from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription


class DataUsageRecord(models.Model):
    """Raw data usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=True)
    kilobytes_used = models.IntegerField(null=False)


class VoiceUsageRecord(models.Model):
    """Raw voice usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=True)
    seconds_used = models.IntegerField(null=False)


class UsageRecord(models.Model):
    """
    Model contains aggregated data from models DataUsageRecord and VoiceUsageRecord.
    price_data - contains sum of DataUsageRecord.price filtered by date
    price_voice - contains sum of VoiceUsageRecord.price filtered by date

    To get total price should be used property UsageRecord.price
    """
    # TODO: attr max_digits for price_data, price_voice should be calculated base on expected usage of this field. Right now it set to 10.
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price_data = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    price_voice = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    date = models.DateField(null=True)

    kilobytes_used = models.IntegerField(null=False, default=0)
    seconds_used = models.IntegerField(null=False, default=0)

    @property
    def price(self):
        return self.price_data + self.price_voice


@receiver(post_save, sender=DataUsageRecord)
def data_usage_aggregate(sender, instance, created, **kwargs):
    if created:
        date = instance.usage_date.date()
        raw_data = {
            'date': date
        }
        if instance.att_subscription_id:
            raw_data['att_subscription_id'] = instance.att_subscription_id
        elif instance.sprint_subscription_id:
            raw_data['sprint_subscription_id'] = instance.sprint_subscription_id
        else:
            return None

        usage_record, created = UsageRecord.objects.get_or_create(**raw_data)
        usage_record.price_data = F('price_data') + instance.price
        usage_record.kilobytes_used = F('kilobytes_used') + instance.kilobytes_used
        usage_record.save(update_fields=['price_data', 'kilobytes_used'])


@receiver(post_save, sender=VoiceUsageRecord)
def voice_usage_aggregate(sender, instance, created, **kwargs):
    if created:
        date = instance.usage_date.date()
        raw_data = {
            'date': date
        }
        if instance.att_subscription_id:
            raw_data['att_subscription_id'] = instance.att_subscription_id
        elif instance.sprint_subscription_id:
            raw_data['sprint_subscription_id'] = instance.sprint_subscription_id
        else:
            return None

        usage_record, created = UsageRecord.objects.get_or_create(**raw_data)
        usage_record.price_voice = F('price_voice') + instance.price
        usage_record.seconds_used = F('seconds_used') + instance.seconds_used
        usage_record.save(update_fields=['price_voice', 'seconds_used'])
