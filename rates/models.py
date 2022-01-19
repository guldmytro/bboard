from django.db import models


class Category(models.Model):
        

class Rate(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тариф')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')
    sub_name = models.CharField(max_length=100, verbose_name='Описание тарифа')

    # quantity
    photos = models.SmallIntegerField(default=1, verbose_name='Фото', help_text='-1 для безлимита')
    videos = models.SmallIntegerField(default=0, verbose_name='Видео', help_text='-1 для безлимита')
    adds = models.SmallIntegerField(default=0, verbose_name='Автоподбросы', help_text='-1 для безлимита')

    # days
    days = models.SmallIntegerField(verbose_name='Количество дней', help_text='-1 для безлимита')

    # bonus
    days_bonus = models.PositiveSmallIntegerField(verbose_name='Бонусное количество дней', default=0)
    photos_bonus = models.PositiveSmallIntegerField(verbose_name='Бонусное количество фото', default=0)
    videos_bonus = models.PositiveSmallIntegerField(verbose_name='Бонусное количество видео', default=0)
    adds_bonus = models.PositiveSmallIntegerField(verbose_name='Бонусное количество автоподбросов', default=0)
    bonus_start = models.DateTimeField(blank=True, null=True)
    bonus_end = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    class Meta:
        ordering = ('-created',)
        verbose_name = ('Тарифный план')
        verbose_name_plural = ('Тарифные планы')

    def __str__(self):
        return self.name


class Toss(models.Model):
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = ('Автоподброс')
        verbose_name_plural = ('Автоподбросы')

    def __str__(self):
        return f'Автоподбросы - {self.quantity} шт.'
    
