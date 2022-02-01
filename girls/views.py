from django.shortcuts import render, get_object_or_404
from .models import Girl, Image, Review, View, Video
from .forms import AddReviewForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from rates.models import Category, Rate
from .forms import SearchForm


def home(request):
    girls_object = Girl.published.all().order_by('-created')
    slug = 'new'
    category_name = 'Новые'
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
        'section': 'home'
    }
    return render(request, 'pages/home.html', context)


def girl_detail(request, id):
    girl = get_object_or_404(Girl, id=id)
    photos = Image.objects.filter(girl=girl)
    videos = Video.objects.filter(girl=girl)
    reviews_objects = Review.objects.all().order_by('-created')
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

    context = {
        'girl': girl,
        'photos': photos,
        'videos': videos,
        'reviews': reviews,
        'add_review_form': add_review_form
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
    if slug:
        category = get_object_or_404(Category, slug=slug)
        rates = Rate.objects.filter(category=category)
        girls_object = girls_object.filter(rate__in=rates)
        category_name = category.name
    else:
        slug = 'new'
        category_name = 'Новые'
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
        'section': 'catalog'
    }
    return render(request, 'pages/catalog.html', context)


def search(request):
    search_form = SearchForm(request.GET)
    is_searching = False
    girls = False
    if search_form.is_valid():
        cd = search_form.cleaned_data
        girls_object = Girl.published.all()
        if cd['city']:
            girls_object = girls_object.filter(city=cd['city'])
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
