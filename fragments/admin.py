from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext as _
from markdownx.admin import MarkdownxModelAdmin

from subscribers.models import Subscriber
from .models import Article


@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    actions = ['publish_article']
    date_hierarchy = 'published'
    list_display = ('title', 'published')
    prepopulated_fields = {"slug": ("title",)}

    def publish_article(self, request, queryset):
        queryset.update(published=timezone.now())

        site = Site.objects.get(name='denklab.org')

        for subscriber in Subscriber.objects.filter(application='fragments', confirmed__isnull=False):
            subscriber.update(last_notified=timezone.now())

            send_mail(_("A new article was published!"),
                      _("A new article was published at https://%s/fragmente\n\n"
                        "If you don't want to receive this updates, unsubscribe here:\n"
                        "https://%s/subscribers/unsubscribe/%s" %
                        (site, site, subscriber.id)),
                      settings.DEFAULT_FROM_EMAIL,
                      [subscriber.email],
                      fail_silently=False)

    publish_article.short_description = _("Publish selected Articles")
