from django.contrib.syndication.views import Feed
from markdownx.utils import markdownify

from fragments.models import Article


class LatestArticlesFeed(Feed):
    title = 'Fragmente'
    link = 'fragmente'
    description = 'Der Versuch die Wiederentdeckung meiner Stadt und meiner Heimat zudokumentieren'

    @staticmethod
    def items():
        return Article.objects.order_by('-published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdownify(item.content)
