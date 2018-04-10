from django.contrib.syndication.views import Feed
from markdownx.utils import markdownify

from blog.models import Entry


class LatestEntriesFeed(Feed):
    title = 'Blog Einträge'
    link = 'blog'
    description = ''

    @staticmethod
    def items():
        return Entry.objects.filter(published__isnull=False).order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdownify(item.content)
