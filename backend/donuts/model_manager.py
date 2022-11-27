from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class DonutManager(models.Manager):

    def get_donuts_by_code(self, codes):
        if not isinstance(codes, set) or len(codes) < 1:
            raise ValidationError('Invalid codes')

        donuts = self.get_queryset().filter(donut_code__in=codes)

        if donuts.count() == len(codes):
            return donuts
        else:
            for donut in donuts:
                codes.discard(donut.donut_code)
            raise ObjectDoesNotExist(
                f"No donut(s) with the following code(s): {codes}"
            )
