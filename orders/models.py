from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    author = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Пользователь')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk}'
    
    def get_total_cost(self):
        return sum(item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    service = models.CharField(max_length=100, verbose_name='Услуга')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')