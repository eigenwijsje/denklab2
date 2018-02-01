from django.urls import path

from .feeds import LatestEntriesFeed
from .views import EntryDetailView, EntryListView

urlpatterns = [
    path('feed/', LatestEntriesFeed()),
    path('<slug:slug>/', EntryDetailView.as_view(), name='entry_detail'),
    path('', EntryListView.as_view(), name='entry_list')
]
