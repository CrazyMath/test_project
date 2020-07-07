from django.conf.urls import url

from wingtel.usage.views import UsageMetrics

urlpatterns = [
    url(r'^usage_metrics/', UsageMetrics.as_view(), name='usage_metrics'),
]
