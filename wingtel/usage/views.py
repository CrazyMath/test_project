from django.db.models import Sum, Q, F
from rest_framework import views
from rest_framework.response import Response

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.serializers import UsageMetricSerializer, UsageParametsValidator


class UsageMetrics(views.APIView):
    """
    Return list subscriptions with metrics total_price and total_usage.
    Base ot metric_type corresponding total_price and total_usage will be calculated, if metric_type is omitted than both
    voice and data metric will be included in total_price and total_usage.

    Accept next parameters:
        from_date:  `ISO 8601` style dates (eg '2013-01-29')
        to_date: `ISO 8601` style dates (eg '2013-01-29')
        metric_type: voice or data
    """

    serializer_class = UsageMetricSerializer

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        raise NotImplementedError(
            'serializer_class should be defined or method get_serializer_class should be overridden.')

    def get(self, request, format=None):

        validated_params = UsageParametsValidator(data=request.GET)
        validated_params.is_valid()

        from_date = validated_params.validated_data.get('from_date', None)
        to_date = validated_params.validated_data.get('to_date', None)
        metric_type = validated_params.validated_data.get('metric_type', None)

        METRIC_FIELDS = {
            'data': {
                'key_price': 'price_data',
                'key_usage': 'kilobytes_used'
            },
            'voice': {
                'key_price': 'price_voice',
                'key_usage': 'seconds_used'
            }
        }

        queryset_filter = None
        if from_date is not None:
            queryset_filter = Q(usagerecord__date__gte=from_date) if queryset_filter is None else queryset_filter & Q(
                usagerecord__date__gte=from_date)
        if to_date is not None:
            queryset_filter = Q(usagerecord__date__lte=to_date) if queryset_filter is None else queryset_filter & Q(
                usagerecord__date__lte=to_date)

        if metric_type is not None and metric_type in METRIC_FIELDS.keys():
            annotation_dict = {
                'total_price': Sum(f"usagerecord__{METRIC_FIELDS[metric_type]['key_price']}", filter=queryset_filter),
                'total_usage': Sum(f"usagerecord__{METRIC_FIELDS[metric_type]['key_usage']}", filter=queryset_filter)
            }
        else:
            annotation_dict = {
                'total_price': Sum(F(f"usagerecord__{METRIC_FIELDS['data']['key_price']}") + F(
                    f"usagerecord__{METRIC_FIELDS['voice']['key_price']}"), filter=queryset_filter),
                'total_usage': Sum(F(f"usagerecord__{METRIC_FIELDS['data']['key_usage']}") + F(
                    f"usagerecord__{METRIC_FIELDS['voice']['key_usage']}"), filter=queryset_filter)
            }

        att_subscription = ATTSubscription.objects.all().annotate(**annotation_dict).filter(total_usage__gte=0)
        sprint_subscription = SprintSubscription.objects.all().annotate(**annotation_dict).filter(total_usage__gte=0)
        serializer_class = self.get_serializer_class()

        # TODO: Need to implement pagination to avoid fetching big amount of data.
        data = serializer_class(list(att_subscription) + list(sprint_subscription), many=True).data
        return Response(data)
