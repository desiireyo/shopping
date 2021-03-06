# Generated by Django 3.0.5 on 2020-04-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopone', '0019_profileuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price1_range', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price2_range', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flag', models.BooleanField(default=True)),
                ('memo', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
