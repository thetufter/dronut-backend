from django.core.exceptions import ObjectDoesNotExist, BadRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from orders.models import Order
from orders.serializers import OrderSerializer, CreateOrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def create_order(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if serializer.is_valid():
            try:
                order = Order.objects.create_order(**serializer.data)
            except ObjectDoesNotExist as e:
                return Response(
                    {'detail': str(e)},
                    status=HTTP_400_BAD_REQUEST,
                )

            return Response(
                OrderSerializer(order).data,
                status=HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def dispatch_order(self, request, id=None):
        order = self.get_object()

        try:
            order.dispatch()
            return Response(
                {'detail': f'{order} has been dispatched'}
            )
        except BadRequest as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
            )
