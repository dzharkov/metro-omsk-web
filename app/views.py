from annoying.decorators import render_to
from app.models import City


@render_to('edit_map.html')
def edit_map(request, city_id):
    return {'city': City.objects.get(id=city_id)}


@render_to('index.html')
def view_city(request, city_id):
    return {'city': City.objects.get(id=city_id)}
