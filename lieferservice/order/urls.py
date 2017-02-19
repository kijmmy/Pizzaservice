from django.conf.urls import url
from .views import *

app_name='order'
urlpatterns = [
    url(r'^$', ListMenu.as_view(), name='menu'),
    url(r'^(?P<slug>[0-9]+)$', ShowMeal.as_view(), name='meal'),
    url(r'^order/$', OrderMeal.as_view(), name='order'),
    url(r'^order/(?P<slug>[0-9]+)$', ShowOrder.as_view(), name='track_order'),
    #here bee cooks!
    url(r'^recipie/(?P<slug>[0-9]+)$', ShowRecipie.as_view(), name='recipie'),
    url(r'^answer/$', ListRecievedOrders.as_view(), name='cooks_orders'),
    url(r'^answer/(?P<slug>[0-9]+)$', ChangeOrderState.as_view(), name='cook_changes')
]
