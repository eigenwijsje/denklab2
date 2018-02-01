from django.urls import path

from .views import ConfirmView, SubscribeView, SuccessfulView, UnsubscribeView

urlpatterns = [
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
    path('subscribe/successful', SuccessfulView.as_view(), name='subscribe_successful'),
    path('confirm/<uuid:id>', ConfirmView.as_view(), name='confirm_subscription'),
    path('confirm/successful', SuccessfulView.as_view(), name='confirm_successful'),
    path('unsubscribe/<uuid:id>', UnsubscribeView.as_view(), name='unsubscribe'),
    path('unsubscribe/successful', SuccessfulView.as_view(), name='unsubscribe_successful'),
]
