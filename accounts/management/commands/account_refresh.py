from django.core.management.base import BaseCommand
from girls.models import Girl, Retention
from rates.models import Rate
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Refresh account status'

    def handle(self, *args, **options):
        today = datetime.datetime.today().date()
        # update adds status
        girls = Girl.objects.filter(active_advertising=False, auto_activation_advertising_at__year__lte=today.year,
                                    auto_activation_advertising_at__month__lte=today.month,
                                    auto_activation_advertising_at__day__lte=today.day)
        girls.update(active_advertising=True)

        # update profile status
        girls = Girl.objects.filter(status='disabled', auto_activate_rate_at__year__lte=today.year,
                                    auto_activate_rate_at__month__lte=today.month,
                                    auto_activate_rate_at__day__lte=today.day)
        for girl in girls:
            last_deactivation = Retention.objects.filter(type='deactivation', profile=girl).first()
            if last_deactivation:
                start_date = datetime.date(last_deactivation.created.year, last_deactivation.created.month,
                                           last_deactivation.created.day)
                days_left = today - start_date
                days_left = days_left.days - 1
                if days_left > 0:
                    old_end_rate_date = datetime.date(girl.rate_end_date.year, girl.rate_end_date.month, girl.rate_end_date.day)
                    girl.rate_end_date = old_end_rate_date + datetime.timedelta(days=days_left)
                    girl.save()
        girls.update(status='published')

        # tariff ended check
        girls = Girl.objects.filter(status='published', rate_end_date__year__lte=today.year,
                                    rate_end_date__month__lte=today.month,
                                    rate_end_date__day__lte=today.day)
        start_tarif = Rate.objects.filter(type='start').first()
        for girl in girls:
            if start_tarif:
                girl.rate = start_tarif
                girl.max_images = start_tarif.photos
                girl.max_videos = start_tarif.videos
                girl.adds_left = start_tarif.adds
                girl.rate_end_date = datetime.date.today() + datetime.timedelta(days=start_tarif.days)
                girl.save()

        # delete old accounts
        users = User.objects.filter(is_staff=False)
        for user in users:
            last_login = datetime.date(user.last_login.year, user.last_login.month,
                                       user.last_login.day)
            days_offline = (today - last_login).days
            if days_offline > 150:
                user.delete()


