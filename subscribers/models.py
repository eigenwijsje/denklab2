import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext as _


class Subscriber(models.Model):
    APPLICATION_CHOICES = (
        ('blog', 'blog'),
        ('fragments', 'fragments'),
    )
    id = models.UUIDField(primary_key=True, editable=False)
    application = models.CharField(max_length=16, choices=APPLICATION_CHOICES, verbose_name=_("Application"))
    email = models.EmailField(verbose_name=_("E-mail address"))
    subscribed = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Date of subscription"))
    confirmed = models.DateTimeField(blank=True, null=True, verbose_name=_("Date of confirmation"))
    last_notified = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=_("Date of last notification"))
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Date of last update"))

    class Meta:
        ordering = ('email',)
        unique_together = ('email', 'application')
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        site = Site.objects.get(name='denklab.org')

        if not self.id:
            self.id = uuid.uuid4()

        super().save(*args, **kwargs)

        if not self.confirmed:
            if self.subscribed > self.last_updated:
                send_mail(_("A subscription awaits your confirmation!"),
                          _("A subscription for https://%s/%s awaits your confirmation!\n"
                            "Click here to confirm it was you:\n"
                            "https://%s/subscribers/confirm/%s" %
                            (site, self.application, site, self.id)),
                          settings.DEFAULT_FROM_EMAIL,
                          [self.email],
                          fail_silently=False)
        else:
            if self.confirmed > self.last_updated:
                entry_or_article = 'entry' if self.application == 'blog' else 'article'

                send_mail(_("Your subscription was confirmed!"),
                          _("Your subscription for https://%s/%s was confirmed!\n"
                            "You will now receive a notification when a new %% is published." %
                            (site, self.application, entry_or_article)),
                          settings.DEFAULT_FROM_EMAIL,
                          [self.email],
                          fail_silently=False)

    def delete(self, using=None, keep_parents=False):
        site = Site.objects.get(name='denklab.org')

        send_mail(_("You canceled your subscription!"),
                  _("You canceled your subscription for https://%s/%s!\n"
                    "This is the last email you'll receive." %
                    (site, self.application)),
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email],
                  fail_silently=False)

        super().delete(using, keep_parents)
