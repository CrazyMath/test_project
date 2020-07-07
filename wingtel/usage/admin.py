from django.contrib import admin

from wingtel.usage.models import DataUsageRecord, VoiceUsageRecord, UsageRecord

# Register your models here.
admin.site.register(DataUsageRecord)
admin.site.register(VoiceUsageRecord)
admin.site.register(UsageRecord)
