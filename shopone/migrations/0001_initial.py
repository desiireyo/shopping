# Generated by Django 3.0.5 on 2020-04-15 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setsubgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Setunit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settypegroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('subgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setsubgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('barcode', models.CharField(max_length=255, unique=True)),
                ('productname', models.TextField(blank=True)),
                ('price_mem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disct_mem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('typdisct_mem', models.BooleanField(default=True)),
                ('netprice_mem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_guest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disct_guest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('typdisct_guest', models.BooleanField(default=True)),
                ('netprice_guest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, upload_to='product')),
                ('stock', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('memo', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setgroup')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setstatus')),
                ('subgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setsubgroup')),
                ('typegroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Settypegroup')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopone.Setunit')),
            ],
        ),
    ]
