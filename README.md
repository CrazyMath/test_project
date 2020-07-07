# WingTel Coding Challenge

## Requirements
* Python 3.7+
* Postgresql

## Challenge

### Aggregated Usage Models

Create models for aggregating subscription usage metrics which will be used for generating metrics and small reports.

We have two types of usage - data usage and voice usage. The raw usage records usage types for these exist in the `DataUsageRecord` and `VoiceUsageRecord` tables. Create models that will use the data from these two tables and store aggregated metrics segmented by date.

**HINT**: Optimize for high volumes of raw usage records, but not long retention periods.

Create one or both of the APIs below:

### API - Subscriptions Exceeding Usage Price Limit

Create an API that accepts a price limit as a request parameter. Find any subscriptions that have reached the price limit on either data and/or voice (check both usage types). Return a list of the subscription id, type(s) of usage that exceeded the price limit, and by how much it's exceeded the limit.

### API - Usage Metrics By Subscription and Usage Type

Create an API that fetches data usage metrics and voice usage metrics by subscription id. This endpoint should accept a from date, to date, and usage type request parameter. Return a list of the subscription id, total price of usage for the given dates, and total usage for any subscriptions that had usage during the given from and to dates.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

### BONUSES

1. Improve and optimize the existing code where you see fit.
2. Write tests!


### DEVELOPER NOTES


To run project with docker for local development(supposed that you have installed docker and docker-compose):

`docker-compose -f local.yml build`

`docker-compose -f local.yml up`


With console next command can be run:

`docker-compose -f local.yml run --rm django python manage.py test --settings=config.settings.test` - to run tests

`docker-compose -f local.yml run --rm django python manage.py createsuperuser` - create superuser

`docker-compose -f local.yml run --rm django python manage.py makemigrations` - to makemigrations

`docker-compose -f local.yml run --rm django python manage.py migrate` - to apply migrations

`docker-compose -f local.yml run --rm django python manage.py shell` - to run shell
