from django.views.generic import DetailView, ListView

from blog.models import Entry


class EntryView(object):
    model = Entry
    queryset = Entry.objects.all()  # filter(published__isnull=False)


class EntryListView(EntryView, ListView):
    pass


class EntryDetailView(EntryView, DetailView):
    pass
