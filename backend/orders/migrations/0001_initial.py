import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donuts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=1024)),
                ('status', models.IntegerField(choices=[
                 (0, 'Created'), (1, 'Dispatched')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1,
                 validators=[django.core.validators.MinValueValidator(1)])),
                ('donut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='order_lines', to='donuts.donut')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='lines', to='orders.order')),
            ],
        ),
        migrations.AddConstraint(
            model_name='orderline',
            constraint=models.UniqueConstraint(
                fields=('order', 'donut'), name='order_and_donut_are_unique'),
        ),
    ]
