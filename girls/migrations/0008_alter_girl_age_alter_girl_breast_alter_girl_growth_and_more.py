# Generated by Django 4.0.1 on 2022-01-21 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('girls', '0007_alter_girl_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='girl',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='girl',
            name='breast',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Грудь'),
        ),
        migrations.AlterField(
            model_name='girl',
            name='growth',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рост'),
        ),
        migrations.AlterField(
            model_name='girl',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='girl',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='girl',
            name='weight',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Вес'),
        ),
    ]
