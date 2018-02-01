from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from markdownx.models import MarkdownxField


class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name=_("Title"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    content = MarkdownxField(verbose_name=_("Content"))
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=_("Date published"))

    class Meta:
        get_latest_by = 'published'
        ordering = ('-published',)
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def __str__(self):
        return self.title
