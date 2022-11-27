import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from donuts.model_manager import DonutManager


class Donut(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    donut_code = models.SlugField(max_length=50, unique=True)

    name = models.CharField(max_length=512)

    description = models.TextField(blank=True)

    price_per_unit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999.99)],
    )

    objects = DonutManager()

    def __str__(self):
        return self.name
