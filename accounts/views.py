from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileEditForm, ProfilePriceEditForm, ProfileServicesEditForm, \
    ProfileCheckPhotoForm, ProfileAdditionalEditForm
from girls.models import Girl, Image, Video, View
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.timezone import datetime


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Girl.objects.create(user=new_user)
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
            profile_price_form.save()
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

