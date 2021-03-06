# Generated by Django 4.0.1 on 2022-01-21 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('girls', '0005_alter_city_options_alter_region_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='girl',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='girl',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('disabled', 'Остановлена'), ('published', 'Опубликована')], default='draft', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
    ]
