from django.urls import path

from fragments.feeds import LatestArticlesFeed
from fragments.views import ArticleDetailView, ArticleListView

urlpatterns = [
    path('feed/', LatestArticlesFeed()),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('', ArticleListView.as_view(), name='article_list'),
]
