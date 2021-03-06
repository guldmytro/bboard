from django.db import models
from django.contrib.auth import get_user_model
from rates.models import Rate

User = get_user_model()


class Order(models.Model):
    author = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Пользователь')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def order_title(self):
        return f'Заказ #{self.pk}'

    def __str__(self):
        return self.order_title()

    def get_total_price(self):
        return sum(item.price for item in self.items.price)
    
    def get_total_cost(self):
        return sum(item.price for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    service = models.CharField(max_length=100, verbose_name='Услуга')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Элемент покупки'
        verbose_name_plural = 'Элементы покупки'


class TariffOrder(models.Model):
    author = models.ForeignKey(User, related_name='tariff_orders', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Пользователь')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def order_title(self):
        return f'Смена тарифа #{self.pk}'

    def get_total_cost(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return self.order_title()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Смена тарифа'
        verbose_name_plural = 'Смены тарифов'


class TariffOrderItem(models.Model):
    order = models.ForeignKey(TariffOrder, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    rate = models.ForeignKey(Rate, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Тариф')
    price = models.IntegerField(verbose_name='Цена')
    videos = models.IntegerField(verbose_name='количество видео')
    photos = models.IntegerField(verbose_name='количество фото')
    adds = models.IntegerField(verbose_name='количесто автоподбросов')
    days = models.IntegerField(verbose_name='Количество дней')

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Элемент покупки'
        verbose_name_plural = 'Элементы покупки'
