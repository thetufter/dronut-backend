from django.urls import path
from orders.views import OrderViewSet


urlpatterns = [
    path(
        '',
        OrderViewSet.as_view({
            'get': 'list',
            'post': 'create_order',
        }),
        name='order-list'
    ),
    path(
        '/<int:id>',
        OrderViewSet.as_view({
            'get': 'retrieve',
            'patch': 'dispatch_order',
        }),
        name='order-detail'
    ),
]
