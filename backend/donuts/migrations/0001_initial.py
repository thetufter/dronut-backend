import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donut',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('donut_code', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('price_per_unit', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[
                 django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999.99)])),
            ],
        ),
    ]
