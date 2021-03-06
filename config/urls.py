"""wingtel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework import routers

from wingtel.att_subscriptions.views import ATTSubscriptionViewSet
from wingtel.plans.views import PlanViewSet
from wingtel.purchases.views import PurchaseViewSet
from wingtel.sprint_subscriptions.views import SprintSubscriptionViewSet

router = routers.DefaultRouter()

router.register(r'att_subscriptions', ATTSubscriptionViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'sprint_subscriptions', SprintSubscriptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
    path(r'api/', include(('wingtel.usage.urls', 'wingtel.usage'), namespace='usage')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
