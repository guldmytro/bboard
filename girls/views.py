from django.shortcuts import render, get_object_or_404
from .models import Girl, Image, Review
from .forms import AddReviewForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def home(request):
    context = {}
    return render(request, 'pages/home.html', context)


def girl_detail(request, id):
    girl = get_object_or_404(Girl, id=id)
    photos = Image.objects.filter(girl=girl)
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

    context = {
        'girl': girl,
        'photos': photos,
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

