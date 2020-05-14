# Generated by Django 3.0.3 on 2020-05-13 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopone', '0036_setourservice_setworktogether'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderalluser',
            name='flagCancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderalluser',
            name='orderno',
            field=models.CharField(default='0', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderalluser',
            name='statusCancel',
            field=models.CharField(default='normal', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderalluseritem',
            name='flagCancel',
            field=models.BooleanField(default=False),
        ),
    ]