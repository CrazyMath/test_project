import random

import factory

from wingtel.plans.models import Plan


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Sequence(lambda n: f'Plan #{n}')
    price = random.randint(1, 100)
    data_available = random.randint(100, 200)
