from django.db import models
from django.utils import timezone
from rates.models import Rate


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Услуга')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name='Район')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Слаг')
    city = models.ForeignKey(City, related_name='regions', on_delete=models.CASCADE, verbose_name='город')

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Girl(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Приостановлена'),
        ('published', 'Опубликована')
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    breast = models.PositiveSmallIntegerField(verbose_name='Грудь')
    growth = models.PositiveSmallIntegerField(verbose_name='Рост')
    weight = models.PositiveSmallIntegerField(verbose_name='Вес')
    about = models.TextField(blank=True, null=True, verbose_name='Информация')
    services = models.ManyToManyField(Service, verbose_name='Услуги', null=True, blank=True, related_name='girls')

    # pricing
    price_30_home = models.PositiveSmallIntegerField(verbose_name='Цена 30 минут (апартаменты)', null=True, blank=True)
    price_1h_home = models.PositiveSmallIntegerField(verbose_name='Цена 1 час (апартаменты)', null=True, blank=True)
    price_2h_home = models.PositiveSmallIntegerField(verbose_name='Цена 2 час (апартаменты)', null=True, blank=True)
    price_night_home = models.PositiveSmallIntegerField(verbose_name='Цена ночь (апартаменты)', null=True, blank=True)
    price_1h_departure = models.PositiveSmallIntegerField(verbose_name='Цена 1 час (выезд)', null=True, blank=True)
    price_2h_departure = models.PositiveSmallIntegerField(verbose_name='Цена 2 час (выезд)', null=True, blank=True)
    price_night_departure = models.PositiveSmallIntegerField(verbose_name='Цена ночь (выезд)', null=True, blank=True)

    # other status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    verified = models.BooleanField(default=False, verbose_name='Реальное фото')
    test_photo = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d', verbose_name='Проверочное фото')
    can_search = models.BooleanField(default=False, verbose_name='Поиск по номеру')

    # additional features
    parking = models.BooleanField(default=False, verbose_name='Парковка')
    apartment = models.BooleanField(default=False, verbose_name='Отдельная квартира')

    # date
    publish = models.DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # contacts
    whatsapp = models.CharField(max_length=300, verbose_name='WhatsApp', blank=True, null=True)
    telegram = models.CharField(max_length=300, verbose_name='Telegram', blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон')

    # limits
    max_images = models.IntegerField(verbose_name='Максимальное количество картинок', default=1)
    max_videos = models.IntegerField(verbose_name='Максимальное количество видео', default=0)
    adds_left = models.IntegerField(verbose_name='Количество подбросов', default=0)

    # adds time
    active_advertising = models.BooleanField(default=False, verbose_name='Активна реклама')
    start_add_at = models.TimeField(blank=True, null=True, verbose_name='Показывать обьявления после')
    timedelta_add = models.PositiveSmallIntegerField(blank=True, null=True,
                                                     verbose_name='Длительность показа обьявления в часах')

    # rate
    rate = models.ForeignKey(Rate, on_delete=models.SET_NULL, verbose_name='Тарифный план')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    body = models.TextField(max_length=400, verbose_name='Текст отзыва')
    girl = models.ForeignKey(Girl, verbose_name='Девушка', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Отзыв {self.name} o {self.girl.name}'


class Video(models.Model):
    file = models.FileField(upload_to='videos/%Y/%m/%d', verbose_name='Видео')
    girl = models.ForeignKey(Girl, related_name='videos', verbose_name='Девушка', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.file.name


class Image(models.Model):
    file = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Фото')
    girl = models.ForeignKey(Girl, related_name='images', verbose_name='Девушка', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.file.name


class View(models.Model):
    TYPE_CHOICES = (
        ('video', 'Видео'),
        ('profile', 'Профиль'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)