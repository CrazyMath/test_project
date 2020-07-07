import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from usage.factories import DataUsageRecordFactory, VoiceUsageRecordFactory
from wingtel.att_subscriptions.factories import ATTSubscriptionFactory


class TestUsageMetrics(APITestCase):

    def setUp(self):
        self.att_subscription = ATTSubscriptionFactory.create()
        self.date = datetime.datetime.now()
        self.data_usage_record_1 = DataUsageRecordFactory.create(att_subscription_id=self.att_subscription,
                                                                 usage_date=self.date)
        self.data_usage_record_2 = DataUsageRecordFactory.create(att_subscription_id=self.att_subscription,
                                                                 usage_date=self.date - datetime.timedelta(days=2))
        self.voice_usage_record_1 = VoiceUsageRecordFactory.create(att_subscription_id=self.att_subscription,
                                                                   usage_date=self.date)
        self.url = reverse('usage:usage_metrics')

    def test_get(self):
        # Check when query is empty
        request_data = {}
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['id'], self.att_subscription.id)
        self.assertEquals(response.json()[0]['total_usage'], self.data_usage_record_1.kilobytes_used +
                          self.data_usage_record_2.kilobytes_used + self.voice_usage_record_1.seconds_used)
        self.assertEquals(response.json()[0]['total_price'], self.data_usage_record_1.price +
                          self.data_usage_record_2.price + self.voice_usage_record_1.price)
        self.assertEquals(response.json()[0]['subscription_type'], 'ATTSubscription')

        # Check when metric_type=data
        request_data = {
            'metric_type': 'data'
        }
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['id'], self.att_subscription.id)
        self.assertEquals(response.json()[0]['total_usage'], self.data_usage_record_1.kilobytes_used +
                          self.data_usage_record_2.kilobytes_used)
        self.assertEquals(response.json()[0]['total_price'], self.data_usage_record_1.price +
                          self.data_usage_record_2.price)
        self.assertEquals(response.json()[0]['subscription_type'], 'ATTSubscription')

        # Check when metric_type=voice
        request_data = {
            'metric_type': 'voice'
        }
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['id'], self.att_subscription.id)
        self.assertEquals(response.json()[0]['total_usage'], self.voice_usage_record_1.seconds_used)
        self.assertEquals(response.json()[0]['total_price'], self.voice_usage_record_1.price)
        self.assertEquals(response.json()[0]['subscription_type'], 'ATTSubscription')

        # Check dates
        request_data = {
            'metric_type': 'data',
            'from_date': self.date.date().isoformat()
        }
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['id'], self.att_subscription.id)
        self.assertEquals(response.json()[0]['total_usage'], self.data_usage_record_1.kilobytes_used)
        self.assertEquals(response.json()[0]['total_price'], self.data_usage_record_1.price)
        self.assertEquals(response.json()[0]['subscription_type'], 'ATTSubscription')

        request_data = {
            'metric_type': 'data',
            'from_date': (self.date - datetime.timedelta(days=2)).date().isoformat(),
            'to_date': (self.date - datetime.timedelta(days=1)).date().isoformat()
        }
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 1)
        self.assertEquals(response.json()[0]['id'], self.att_subscription.id)
        self.assertEquals(response.json()[0]['total_usage'], self.data_usage_record_2.kilobytes_used)
        self.assertEquals(response.json()[0]['total_price'], self.data_usage_record_2.price)
        self.assertEquals(response.json()[0]['subscription_type'], 'ATTSubscription')

        request_data = {
            'metric_type': 'data',
            'from_date': (self.date - datetime.timedelta(days=4)).date().isoformat(),
            'to_date': (self.date - datetime.timedelta(days=3)).date().isoformat()
        }
        response = self.client.get(self.url, request_data)
        self.assertEquals(len(response.json()), 0)
