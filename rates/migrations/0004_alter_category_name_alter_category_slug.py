# Generated by Django 4.0.1 on 2022-01-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0003_alter_toss_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Слаг'),
        ),
    ]
