from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Client(models.Model):
    phone = models.CharField(max_length=30, db_index=True, verbose_name='Телефон', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.phone


class Review(models.Model):
    RATE_CHOICES = (
        ('bad', 'Гемор'),
        ('inert', 'Не был'),
        ('good', 'Проходящий')
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Автор', related_name='reviews')
    body = models.TextField(max_length=200, verbose_name='Отзыв')
    type = models.CharField(max_length=10, choices=RATE_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Revise(models.Model):
    created = models.DateTimeField(auto_now_add=True)
