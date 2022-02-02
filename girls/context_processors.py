from rates.models import Category
from .models import City
from .utils import get_current_city
from django.db.models import Count, Q


def category_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}


def cities_processor(request):
    cities = City.objects.annotate(cnt=Count('girls', filter=Q(girls__status='published'))).filter(cnt__gt=0)
    city = get_current_city(request)
    return {'cities': cities,
            'city': city}
