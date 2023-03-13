from django.shortcuts import render, get_object_or_404
from .models import Girl, Image, Review, View, Video, Service
from .forms import AddReviewForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from rates.models import Category, Rate
from .forms import SearchForm
from .utils import filter_by_city, get_current_city
from random import shuffle
from django.db.models import F
import datetime
from django.utils.translation import gettext_lazy as _


def home(request):
    # today = datetime.datetime.today().date()
    # end_date = datetime.date(year=2022, month=2, day=22)
    # if today > end_date:
    #     return render(request, 'list.html', {})
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    slug = 'new'
    category_name = 'Новые | New | חָדָשׁ'
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)

    lux_tariffs = Rate.objects.filter(type='lux')
    lux_tariffs = list(rate.id for rate in lux_tariffs)
    lux_girls = Girl.published.filter(rate_id__in=lux_tariffs)
    lux_girls = filter_by_city(request, lux_girls)
    context = {
        'category_name': category_name,
        'lux_girls': lux_girls,
        'slug': slug,
        'girls': girls,
        'section': 'home'
    }
    return render(request, 'pages/home.html', context)


def girl_detail(request, id):
    girl = get_object_or_404(Girl, id=id)
    if girl.max_images == -1:
        photos = Image.objects.filter(girl=girl)
    else:
        photos = Image.objects.filter(girl=girl)[:girl.max_images]
    if girl.max_videos == -1:
        videos = Video.objects.filter(girl=girl)
    else:
        videos = Video.objects.filter(girl=girl)[:girl.max_videos]
    reviews_objects = girl.reviews.all().order_by('-created')
    paginator = Paginator(reviews_objects, 12)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    add_review_form = AddReviewForm()
    if (request.user.is_authenticated and request.user.girl != girl) or not request.user.is_authenticated:
        View.objects.create(type='profile', profile=girl)
    related_girls = list(Girl.published.exclude(id=girl.id).filter(city=girl.city)[:10])
    shuffle(related_girls)
    context = {
        'girl': girl,
        'photos': photos,
        'videos': videos,
        'reviews': reviews,
        'add_review_form': add_review_form,
        'related_girls': related_girls
    }
    return render(request, 'girls/girl_detail.html', context)


@require_POST
def girl_add_review(request, id):
    add_review_form = AddReviewForm(request.POST)
    if add_review_form.is_valid():
        review = add_review_form.save(commit=False)
        girl = get_object_or_404(Girl, id=id)
        review.girl = girl
        review.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'bad'})


@require_POST
@login_required
def girl_delete_review(request, girl_id, review_id):
    girl = request.user.girl
    if not girl.can_delete_comments:
        return JsonResponse({'status': 'bad'})
    review = get_object_or_404(Review, pk=review_id)
    if review.girl == girl:
        review.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad'})


@require_POST
def girl_update_video_cnt(request, girl_id):
    girl = get_object_or_404(Girl, id=girl_id)
    if request.user.is_authenticated and request.user.girl != girl or not request.user.is_authenticated:
        View.objects.create(profile=girl, type='video')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad'})


def catalog(request, slug=None):
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        rates = Rate.objects.filter(category=category)
        girls_object = girls_object.filter(rate__in=rates)
        category_name = category.name
    else:
        slug = 'new'
        category_name = 'Новые | New | חָדָשׁ'

    force_girls_list = None
    if girls_object.count() > 20:
        force_girls_list = list(girls_object.filter(active_advertising=True, adds_left__gt=0))
        shuffle(force_girls_list)
        force_girls_list = force_girls_list[:10]
        force_girls_ids = list(girl.id for girl in force_girls_list)
        girls_object = girls_object.exclude(id__in=force_girls_ids)
        if not request.user.is_authenticated:
            for force_girl in force_girls_list:
                force_girl.adds_left = F('adds_left') - 1
                force_girl.save()
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)
    context = {
        'category_name': category_name,
        'slug': slug,
        'girls': girls,
        'force_girls_list': force_girls_list,
        'section': 'catalog'
    }
    return render(request, 'pages/catalog.html', context)


def search(request):
    search_form = SearchForm(request.GET)
    is_searching = False
    girls = False
    if search_form.is_valid():
        cd = search_form.cleaned_data
        girls_object = Girl.published.all().order_by('-created')
        girls_object = filter_by_city(request, girls_object)
        if cd['age']:
            girls_object = girls_object.filter(age=cd['age'])
        if cd['price_from']:
            girls_object = girls_object.filter(min_price__gte=int(cd['price_from']))
        if cd['price_to']:
            girls_object = girls_object.filter(max_price__lte=int(cd['price_to']))
        if cd['apartments']:
            girls_object = girls_object.filter(apartment=True)
        if cd['arrive']:
            girls_object = girls_object.filter(arrive=True)
        if cd['search']:
            is_searching = True
        paginator = Paginator(girls_object, 15)
        page = request.GET.get('page')
        try:
            girls = paginator.page(page)
        except PageNotAnInteger:
            girls = paginator.page(1)
        except EmptyPage:
            girls = paginator.page(paginator.num_pages)

    context = {
        'is_searching': is_searching,
        'girls': girls,
        'search_form': search_form
    }
    return render(request, 'pages/search.html', context)


@require_POST
def city(request):
    request.session['city'] = request.POST.get('slug')
    return JsonResponse({'status': 'ok'})


def catalog_by_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    girls_object = girls_object.filter(services=service)
    category_name = service.name
    force_girls_list = None
    if girls_object.count() > 20:
        force_girls_list = list(girls_object.filter(active_advertising=True, adds_left__gt=0))
        shuffle(force_girls_list)
        force_girls_list = force_girls_list[:10]
        force_girls_ids = list(girl.id for girl in force_girls_list)
        girls_object = girls_object.exclude(id__in=force_girls_ids)
        if not request.user.is_authenticated:
            for force_girl in force_girls_list:
                force_girl.adds_left = F('adds_left') - 1
                force_girl.save()
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)

    context = {
        'category_name': category_name,
        'slug': slug,
        'girls': girls,
        'force_girls_list': force_girls_list,
        'section': 'catalog'
    }
    return render(request, 'pages/catalog.html', context)


def catalog_real_photo(request):
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    girls_object = girls_object.filter(verified=True)
    category_name = _('Real photo')
    force_girls_list = None
    if girls_object.count() > 20:
        force_girls_list = list(girls_object.filter(active_advertising=True, adds_left__gt=0))
        shuffle(force_girls_list)
        force_girls_list = force_girls_list[:10]
        force_girls_ids = list(girl.id for girl in force_girls_list)
        girls_object = girls_object.exclude(id__in=force_girls_ids)
        if not request.user.is_authenticated:
            for force_girl in force_girls_list:
                force_girl.adds_left = F('adds_left') - 1
                force_girl.save()
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)
    slug = 'real-photo'
    context = {
        'category_name': category_name,
        'slug': 'by-real-photo',
        'girls': girls,
        'force_girls_list': force_girls_list,
        'section': 'catalog',
        'slug': slug
    }
    return render(request, 'pages/catalog.html', context)


def catalog_outcall(request):
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    girls_object = girls_object.filter(verified=True)
    category_name = _('Outcall')
    force_girls_list = None
    if girls_object.count() > 20:
        force_girls_list = list(girls_object.filter(active_advertising=True, adds_left__gt=0))
        shuffle(force_girls_list)
        force_girls_list = force_girls_list[:10]
        force_girls_ids = list(girl.id for girl in force_girls_list)
        girls_object = girls_object.exclude(id__in=force_girls_ids)
        if not request.user.is_authenticated:
            for force_girl in force_girls_list:
                force_girl.adds_left = F('adds_left') - 1
                force_girl.save()
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)
    slug = 'outcall'
    context = {
        'category_name': category_name,
        'slug': 'by-real-photo',
        'girls': girls,
        'force_girls_list': force_girls_list,
        'section': 'catalog',
        'slug': slug
    }
    return render(request, 'pages/catalog.html', context)


def catalog_apartment(request):
    girls_object = Girl.published.all().order_by('-created')
    girls_object = filter_by_city(request, girls_object)
    girls_object = girls_object.filter(verified=True)
    category_name = _('Separate Apartment')
    force_girls_list = None
    if girls_object.count() > 20:
        force_girls_list = list(girls_object.filter(active_advertising=True, adds_left__gt=0))
        shuffle(force_girls_list)
        force_girls_list = force_girls_list[:10]
        force_girls_ids = list(girl.id for girl in force_girls_list)
        girls_object = girls_object.exclude(id__in=force_girls_ids)
        if not request.user.is_authenticated:
            for force_girl in force_girls_list:
                force_girl.adds_left = F('adds_left') - 1
                force_girl.save()
    paginator = Paginator(girls_object, 15)
    page = request.GET.get('page')
    try:
        girls = paginator.page(page)
    except PageNotAnInteger:
        girls = paginator.page(1)
    except EmptyPage:
        girls = paginator.page(paginator.num_pages)
    slug = 'apartment'
    context = {
        'category_name': category_name,
        'slug': 'by-real-photo',
        'girls': girls,
        'force_girls_list': force_girls_list,
        'section': 'catalog',
        'slug': slug
    }
    return render(request, 'pages/catalog.html', context)
