# Generated by Django 4.0.1 on 2022-01-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('girls', '0012_rename_arive_girl_arrive'),
    ]

    operations = [
        migrations.AddField(
            model_name='girl',
            name='max_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Максимальная цена'),
        ),
        migrations.AddField(
            model_name='girl',
            name='min_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Минимальная цена'),
        ),
    ]
