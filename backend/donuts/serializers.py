from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from donuts.models import Donut


class DonutSerializer(serializers.ModelSerializer):
    donut_code = serializers.SlugField(
        max_length=50,
        min_length=1,
        validators=[UniqueValidator(queryset=Donut.objects.all())]
    )

    class Meta:
        model = Donut
        fields = [
            'id',
            'donut_code',
            'name',
            'description',
            'price_per_unit',
        ]
        read_only_fields = ['id']


class DonutShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donut
        fields = [
            'donut_code',
            'name',
            'price_per_unit',
        ]
