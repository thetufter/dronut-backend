from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from donuts.models import Donut
from donuts.serializers import DonutSerializer


class DonutViewSet(ModelViewSet):
    queryset = Donut.objects.all()
    serializer_class = DonutSerializer
    lookup_field = 'id'
    filter_backends = [SearchFilter]
    search_fields = ['^donut_code']
