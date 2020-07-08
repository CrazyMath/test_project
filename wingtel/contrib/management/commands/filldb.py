# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import sys
from django.core.management import BaseCommand

from att_subscriptions.factories import ATTSubscriptionFactory, UserFactory
from usage.factories import VoiceUsageRecordFactory, DataUsageRecordFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stdout.write('Started fill db\r\n')
        UserFactory.create_batch(5)
        sys.stdout.write('Created 5 User.\r\n')
        ATTSubscriptionFactory.create_batch(5)
        sys.stdout.write('Created 5 ATTSubscription.\r\n')
        VoiceUsageRecordFactory.create_batch(100)
        sys.stdout.write('Created 100 VoiceUsageRecord.\r\n')
        DataUsageRecordFactory.create_batch(100)
        sys.stdout.write('Created 100 DataUsageRecordFactory.\r\n')

        sys.stdout.write('Completed fill db\r\n')
