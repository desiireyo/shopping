# Generated by Django 3.0.5 on 2020-04-19 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopone', '0011_auto_20200420_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setgroup',
            name='code',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='setgroup',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='setgroup',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]
