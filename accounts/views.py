from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileEditForm, ProfilePriceEditForm, ProfileServicesEditForm, \
    ProfileCheckPhotoForm, ProfileAdditionalEditForm, CheckPhoneForm, ClientForm, ClientReviewForm, RateForm
from girls.models import Girl, Image, Video, View
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.timezone import datetime
from clients.models import Client, Revise, Review
import re
from orders.models import Order, OrderItem, TariffOrderItem, TariffOrder
from rates.models import Toss
from django.urls import reverse
from django.db.models import F
from django.conf import settings
import datetime as _dt
from rates.models import Rate


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            girl = Girl.objects.create(user=new_user)
            try:
                start_tarif = Rate.objects.filter(type='start').first()
                if start_tarif:
                    girl.rate = start_tarif
                    girl.max_images = start_tarif.photos
                    girl.max_videos = start_tarif.videos
                    girl.adds_left = start_tarif.adds
                    girl.rate_end_date = _dt.date.today() + _dt.timedelta(days=start_tarif.days)
                    girl.save()
            except:
                pass
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    girl = request.user.girl
    all_views = View.objects.filter(profile=girl, type='profile').count()
    today = datetime.today()
    last_day_views = View.objects.filter(profile=girl, type='profile',
                                         created__year=today.year,
                                         created__month=today.month,
                                         created__day=today.day).count()
    video_views = View.objects.filter(profile=girl, type='video').count()
    context = {
        'all_views': all_views,
        'last_day_views': last_day_views,
        'video_views': video_views,
        'section': 'dashboard'
    }
    return render(request, 'account/dashboard.html', context)


@login_required
def blacklist(request):
    clients_cnt = Client.objects.all().count()
    clients_checked = Revise.objects.all().count()
    today = datetime.today()
    last_day_checks = Revise.objects.filter(created__year=today.year,
                                            created__month=today.month,
                                            created__day=today.day).count()
    check_phone_form = CheckPhoneForm()
    client_form = ClientForm()
    client_review_form = ClientReviewForm()
    context = {
        'last_day_checks': last_day_checks,
        'clients_cnt': clients_cnt,
        'clients_checked': clients_checked,
        'check_phone_form': check_phone_form,
        'client_form': client_form,
        'client_review_form': client_review_form,
        'section': 'blacklist'
    }
    return render(request, 'account/blacklist.html', context)


@login_required
def profile(request):
    girl = request.user.girl
    profile_form = ProfileEditForm(instance=girl)
    profile_price_form = ProfilePriceEditForm(instance=girl)
    profile_service_form = ProfileServicesEditForm(instance=girl)
    profile_check_photo_form = ProfileCheckPhotoForm(instance=girl)
    profile_additional_form = ProfileAdditionalEditForm(instance=girl)
    photos = Image.objects.filter(girl=girl)
    videos = Video.objects.filter(girl=girl)
    context = {
        'profile_form': profile_form,
        'profile_price_form': profile_price_form,
        'profile_service_form': profile_service_form,
        'profile_check_photo_form': profile_check_photo_form,
        'profile_additional_form': profile_additional_form,
        'photos': photos,
        'videos': videos,
        'section': 'profile',
    }
    return render(request, 'account/profile.html', context)


@require_POST
@login_required
def profile_update_info(request):
    profile_form = ProfileEditForm(request.POST, instance=request.user.girl)
    if profile_form.is_valid():
        if profile_form.has_changed():
            profile_form.save()
            if request.user.girl.status == 'draft':
                request.user.girl.status = 'published'
                request.user.girl.save()
            messages.success(request, 'Ваш профиль был успешно обновлен')
    else:
        messages.error(request, 'Ошибка обновления профиля')
    return redirect('profile')


@require_POST
@login_required
def prifile_update_price(request):
    profile_price_form = ProfilePriceEditForm(request.POST, instance=request.user.girl)
    if profile_price_form.is_valid():
        if profile_price_form.has_changed():
            cd = profile_price_form.cleaned_data
            price_list = []
            for key in cd:
                price = cd[key]
                if price:
                    price_list.append(price)
            profile_price_form.save()
            if len(price_list):
                min_price = min(price_list)
                max_price = max(price_list)
                request.user.girl.min_price = min_price
                request.user.girl.max_price = max_price
                request.user.girl.save()
            messages.success(request, 'Ваш профиль был успешно обновлен')
    else:
        messages.error(request, 'Ошибка обновления профиля')
    return redirect('profile')


@require_POST
@login_required
def profile_update_services(request):
    profile_service_form = ProfileServicesEditForm(request.POST, instance=request.user.girl)
    profile_additional_form = ProfileAdditionalEditForm(request.POST, instance=request.user.girl)
    if profile_service_form.is_valid() and profile_additional_form.is_valid():
        if profile_service_form.has_changed() or profile_additional_form.has_changed():
            profile_service_form.save()
            profile_additional_form.save()
            messages.success(request, 'Список Ваших услуг был успешно обновлен')
    else:
        messages.error(request, 'Ошибка обновления профиля')
    return redirect('profile')


@require_POST
@login_required
def profile_send_test_photo(request):
    image = request.FILES.get('0')
    if image:
        request.user.girl.test_photo = image
        request.user.girl.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'bad'})


@require_POST
@login_required
def profile_delete_test_photo(request):
    request.user.girl.test_photo = None
    request.user.girl.save()
    return JsonResponse({'status': 'ok'})


@require_POST
@login_required
def profile_send_photos(request):
    profile = request.user.girl
    max_photos = profile.max_images
    images = Image.objects.filter(girl=profile)
    if max_photos == -1 or images.count() < max_photos:
        file_img = request.FILES.get('0')
        if file_img:
            img = Image(file=file_img, girl=request.user.girl)
            img.save()
            return JsonResponse({'status': 'ok', 'id': img.id})
        else:
            return JsonResponse({'status': 'bad'})
    else:
        return JsonResponse({'status': 'forbidden',
                             'text': 'Превышен лимит загрузок'})


@require_POST
@login_required
def profile_delete_photo(request):
    image_id = request.POST.get('id')
    if image_id:
        try:
            image = Image.objects.get(girl=request.user.girl, id=image_id)
            image.delete()
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'bad'})
    else:
        return JsonResponse({'status': 'bad'})


@require_POST
@login_required
def profile_send_video(request):
    profile = request.user.girl
    max_videos = profile.max_videos
    images = Video.objects.filter(girl=profile)
    if max_videos == -1 or images.count() < max_videos:
        file_video = request.FILES.get('0')
        if file_video:
            video = Video(file=file_video, girl=request.user.girl)
            video.save()
            return JsonResponse({'status': 'ok', 'id': video.id,
                                 'url': video.file.url})
        else:
            return JsonResponse({'status': 'bad'})
    else:
        return JsonResponse({'status': 'forbidden',
                             'text': 'Превышен лимит загрузок'})


@require_POST
@login_required
def profile_delete_video(request):
    video_id = request.POST.get('id')
    if video_id:
        try:
            video = Video.objects.get(girl=request.user.girl, id=video_id)
            video.delete()
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'bad'})
    else:
        return JsonResponse({'status': 'bad'})


@require_POST
@login_required
def profile_check_phone(request):
    if not request.user.girl.can_search:
        return JsonResponse({'status': 'bad'})
    phone_form = CheckPhoneForm(request.POST)
    if phone_form.is_valid():
        phone = phone_form.cleaned_data['phone']
        phone = re.sub('[^0-9]', '', phone)
        client = Client.objects.filter(phone__contains=phone).first()
        reviews = Review.objects.filter(client=client)[:10]
        if reviews.count():
            Revise.objects.create()
        context = {
            'reviews': reviews
        }
        return render(request, 'account/reviews.html', context)
    else:
        return JsonResponse({'status': 'bad'})


@require_POST
@login_required
def profile_add_phone(request):
    client_form = ClientForm(request.POST)
    client_review_form = ClientReviewForm(request.POST)
    if client_form.is_valid() and client_review_form.is_valid():
        phone = client_form.cleaned_data['phone']
        phone = re.sub('[^0-9]', '', phone)
        client, created = Client.objects.get_or_create(phone=phone)
        review = client_review_form.save(commit=False)
        review.client = client
        review.author = request.user
        review.save()
        messages.success(request, 'Отзыв успешно добавлен!')

    else:
        messages.success(request, 'Ошибка добавления отзыва...')
    return redirect('blacklist')


@login_required
def push(request):
    rate_form = RateForm(instance=request.user.girl)
    tosses = Toss.objects.all().order_by('price')
    adds_left = request.user.girl.adds_left
    context = {
        'adds_left': adds_left,
        'rate_form': rate_form,
        'tosses': tosses,
        'section': 'push'
    }
    return render(request, 'account/push.html', context)


@login_required
def create_order(request, order_id):
    toss = get_object_or_404(Toss, pk=order_id)
    order = Order.objects.create(author=request.user)
    order_item = OrderItem.objects.create(order=order, service=f'{toss.quantity} автоподбросов', price=toss.price,
                                          quantity=toss.quantity)
    return redirect('push-pay', order.pk)


@login_required
def push_pay(request, order_id):
    order = get_object_or_404(Order, author=request.user, paid=False, pk=order_id)
    paypal_api = settings.PAYPAL_API
    context = {
        'paypal_api': paypal_api,
        'order': order
    }
    return render(request, 'account/push-pay.html', context)


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, author=request.user, paid=False, pk=order_id)
    order.paid = True
    order.save()
    girl = request.user.girl
    tosses_cnt = order.get_total_quantity()
    girl.adds_left = F('adds_left') + tosses_cnt
    girl.save()
    redirect_link = reverse('push-pay-done', kwargs={'order_id': order.id})
    return JsonResponse({'status': 'ok', 'redirect': redirect_link})


@login_required
def push_pay_done(request, order_id):
    order = get_object_or_404(Order, author=request.user, paid=True, pk=order_id)
    return render(request, 'account/push-pay-done.html', {'order': order})


@login_required
@require_POST
def update_adds_time(request):
    girl = request.user.girl
    rate_form = RateForm(request.POST, instance=girl)
    if rate_form.is_valid():
        rate_form.save()
        girl.auto_activation_advertising_at = _dt.date.today() + _dt.timedelta(days=15)
        girl.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'bad'})


@login_required
def tarifs(request):
    adds_left = request.user.girl.adds_left
    rates = Rate.objects.all().exclude(type='start').order_by('price')
    context = {
        'rates': rates,
        'adds_left': adds_left
    }
    return render(request, 'account/tarifs.html', context)


@login_required
def create_tarif_order(request, tariff_id):
    rate = get_object_or_404(Rate, pk=tariff_id)
    order = TariffOrder.objects.create(author=request.user)
    order_item = TariffOrderItem.objects.create(order=order, rate=rate, price=rate.price,
                                                videos=rate.videos, photos=rate.photos, adds=rate.adds, days=rate.days)
    return redirect('tarif-pay', order.pk)


@login_required
def tarif_pay(request, tarif_order_id):
    order = get_object_or_404(TariffOrder, author=request.user, paid=False, pk=tarif_order_id)
    paypal_api = settings.PAYPAL_API
    context = {
        'paypal_api': paypal_api,
        'order': order
    }
    return render(request, 'account/tarif-pay.html', context)


@login_required
def update_tarif_order(request, order_id):
    order = get_object_or_404(TariffOrder, author=request.user, paid=False, pk=order_id)
    order.paid = True
    order.save()
    girl = request.user.girl
    rate = order.items.all().first()
    girl.adds_left = F('adds_left') + rate.adds
    girl.max_images = rate.photos
    girl.max_videos = rate.videos
    end_date = _dt.date.today() + _dt.timedelta(days=rate.days)
    girl.rate_end_date = end_date
    girl.rate = rate.rate
    girl.save()
    redirect_link = reverse('tariff-pay-done', kwargs={'order_id': order.id})
    return JsonResponse({'status': 'ok', 'redirect': redirect_link})


@login_required
def tarif_pay_done(request, order_id):
    order = get_object_or_404(TariffOrder, author=request.user, paid=True, pk=order_id)
    return render(request, 'account/tarif-pay-done.html', {'order': order})

