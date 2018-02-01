from django.views.generic import DetailView, ListView

from fragments.models import Article


class ArticleView(object):
    model = Article
    queryset = Article.objects.filter(published__isnull=False)


class ArticleListView(ArticleView, ListView):
    pass


class ArticleDetailView(ArticleView, DetailView):
    pass
