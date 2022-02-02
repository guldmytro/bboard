from .models import City


def get_current_city(request):
    city = None
    current_city_slug = request.session.get('city')
    if current_city_slug:
        try:
            city = City.objects.get(slug=current_city_slug)
        except City.DoesNotExist:
            city = None
    return city


def filter_by_city(request, objects):
    city = get_current_city(request)
    if city:
        objects = objects.filter(city=city)
    return objects

