from django.contrib import admin
from donuts.models import Donut


@admin.register(Donut)
class DonutAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'donut_code', 'name', 'price_per_unit')
