from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext as _
from markdownx.admin import MarkdownxModelAdmin

from subscribers.models import Subscriber
from .models import Entry


@admin.register(Entry)
class EntryAdmin(MarkdownxModelAdmin):
    actions = ['publish_entry']
    date_hierarchy = 'published'
    list_display = ('title', 'published')
    prepopulated_fields = {"slug": ("title",)}

    def publish_entry(self, request, queryset):
        queryset.update(published=timezone.now())

        site = Site.objects.get(name='denklab.org')

        for subscriber in Subscriber.objects.filter(application='blog', confirmed__isnull=False):
            subscriber.update(last_notified=timezone.now())

            send_mail(_("A new entry was published!"),
                      _("A new entry was published at https://%s/blog\n\n"
                        "If you don't want to receive this updates, unsubscribe here:\n"
                        "https://%s/subscribers/unsubscribe/%s" %
                        (site, site, subscriber.id)),
                      settings.DEFAULT_FROM_EMAIL,
                      [subscriber.email],
                      fail_silently=False)

    publish_entry.short_description = _("Publish selected Entries")
