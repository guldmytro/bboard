from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileEditForm, ProfilePriceEditForm, ProfileServicesEditForm, \
    ProfileCheckPhotoForm
from girls.models import Girl
from django.contrib import messages
from django.views.decorators.http import require_POST


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
    context = {
        'section': 'dashboard'
    }
    return render(request, 'account/dashboard.html', context)


@login_required
def profile(request):
    profile_form = ProfileEditForm(instance=request.user.girl)
    profile_price_form = ProfilePriceEditForm(instance=request.user.girl)
    profile_service_form = ProfileServicesEditForm(instance=request.user.girl)
    profile_check_photo_form = ProfileCheckPhotoForm(instance=request.user.girl)
    context = {
        'profile_form': profile_form,
        'profile_price_form': profile_price_form,
        'profile_service_form': profile_service_form,
        'profile_check_photo_form': profile_check_photo_form,
        'section': 'profile'
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
    if profile_service_form.is_valid():
        if profile_service_form.has_changed():
            profile_service_form.save()
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
