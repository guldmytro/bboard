from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория', unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('girls:catalog_by_slug', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Rate(models.Model):
    RATE_TYPES = (
        ('start', 'Стартовый'),
        ('lux', 'Люксовый')
    )
    name = models.CharField(max_length=100, verbose_name='Тариф')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')
    sub_name = models.TextField(max_length=300, verbose_name='Описание тарифа')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='rates',
                                 verbose_name='Категория')

    # quantity
    photos = models.SmallIntegerField(default=1, verbose_name='Фото', help_text='-1 для безлимита')
    videos = models.SmallIntegerField(default=0, verbose_name='Видео', help_text='-1 для безлимита')
    adds = models.SmallIntegerField(default=0, verbose_name='Автоподбросы', help_text='-1 для безлимита')

    # days
    days = models.SmallIntegerField(verbose_name='Количество дней', help_text='-1 для безлимита')
    type = models.TextField(verbose_name='Тип тарифа', choices=RATE_TYPES, default='', blank=True, null=True)

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
        ordering = ('quantity',)
        verbose_name = ('Автоподброс')
        verbose_name_plural = ('Автоподбросы')

    def __str__(self):
        return f'Автоподбросы - {self.quantity} шт.'
    
