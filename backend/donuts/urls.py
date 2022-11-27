from django.urls import path
from donuts.views import DonutViewSet


urlpatterns = [
    path(
        '',
        DonutViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='donut-list'
    ),
    path(
        '/<uuid:id>',
        DonutViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
        }),
        name='donut-detail'
    ),
]
