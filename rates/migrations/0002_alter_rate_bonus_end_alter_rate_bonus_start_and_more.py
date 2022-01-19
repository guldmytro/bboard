# Generated by Django 4.0.1 on 2022-01-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='bonus_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Окончание акции'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='bonus_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Начало акции'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='sub_name',
            field=models.TextField(max_length=300, verbose_name='Описание тарифа'),
        ),
    ]