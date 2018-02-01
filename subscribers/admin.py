from django.contrib import admin

from subscribers.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'application', 'confirmed', 'last_notified')
    readonly_fields = ('email', 'application', 'confirmed')
