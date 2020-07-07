import random

import factory
from django.contrib.auth import get_user_model

from wingtel.plans.models import Plan
from wingtel.plans.factories import PlanFactory
from wingtel.att_subscriptions.models import ATTSubscription

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    @factory.sequence
    def username(n):
        return f'username_{n}'

    @factory.sequence
    def email(n):
        return f'email_{n}@example.com'

    password = factory.PostGenerationMethodCall('set_password', 'test1234')


class ATTSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ATTSubscription

    @factory.lazy_attribute
    def user(self):
        if not User.objects.all().exists():
            UserFactory.create_batch(5)
        users = User.objects.all()
        return random.choice(users)

    @factory.lazy_attribute
    def plan(self):
        if not Plan.objects.all().exists():
            PlanFactory.create_batch(5)
        plans = Plan.objects.all()
        return random.choice(plans)

    status = 'new'
