from rest_framework import serializers


class UsageParametsValidator(serializers.Serializer):
    """
    This serializer is used to validate request data.
    """
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    metric_type = serializers.ChoiceField(choices=['data', 'voice'], required=False)


class UsageMetricSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    subscription_type = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_usage = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_subscription_type(self, obj):
        """
        Returns name of subscription model type. It's necessary to differentiate different kind subscriptions.
        :param obj: ATTSubscription or SprintSubscription
        :return: str name of class
        """
        return obj.__class__.__name__

    def get_total_price(self, obj):
        if hasattr(obj, 'total_price'):
            return obj.total_price
        return 'N/A'

    def get_total_usage(self, obj):
        if hasattr(obj, 'total_usage'):
            return obj.total_usage
        return 'N/A'
