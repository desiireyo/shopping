# Generated by Django 3.0.5 on 2020-05-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopone', '0027_auto_20200506_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='setproducttopromotion',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
