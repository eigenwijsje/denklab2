from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import Subscriber


class SubscribeView(CreateView):
    model = Subscriber
    fields = ['email', 'application']
    success_url = 'subscribe/successful'
    template_name = 'subscribers/subscribe.html'

    def form_valid(self, form):
        return super().form_valid(form)


class SuccessfulView(TemplateView):
    template_name = 'subscribers/successful.html'
    extra_context = {'action': 'subscribe'}


class ConfirmView(SuccessfulView):
    extra_context = {'action': 'confirm'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            subscriber = Subscriber.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            pass
        else:
            subscriber.confirmed = timezone.now()
            subscriber.save()

        return context


class UnsubscribeView(SuccessfulView):
    extra_context = {'action': 'unsubscribe'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            subscriber = Subscriber.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            pass
        else:
            subscriber.delete()

        return context
