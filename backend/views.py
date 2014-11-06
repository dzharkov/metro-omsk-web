from annoying.decorators import ajax_request
from app.models import City, Station, Line
from django.views.decorators.csrf import csrf_exempt


@ajax_request
def get_card(request, city_id):
    city = City.objects.get(id=city_id)
    return city.as_dict()


def update_station(station, request):
    station.name = request.POST['name']
    station.line = Line.objects.get(id=request.POST['line'])

    if request.POST['next_time']:
        station.next_time = request.POST['next_time']

    station.lt_coord = request.POST['lt']
    station.ln_coord = request.POST['ln']
    station.x_coord = 0
    station.y_coord = 0

    if request.POST['next_id']:
        next_station = Station.objects.get(id=request.POST['next_id'])
        prev_station = next_station.prev_station if hasattr(next_station, 'prev_station') else None
        station.next_station = next_station
    else:
        prev_stations = Station.objects.filter(line=station.line, next_station__isnull=True).all()
        prev_station = None if len(prev_stations) == 0 else prev_stations[0]

    need_update_prev = prev_station is not None and prev_station.id != station.id

    if need_update_prev:
        prev_station.next_station = None
        prev_station.save()

    station.save()

    if need_update_prev:
        prev_station.next_station = station
        prev_station.save()


@ajax_request
def add_station(request):
    station = Station()

    update_station(station, request)

    return {'result': 1}


@ajax_request
def edit_station(request, id):
    station = Station.objects.get(id=id)
    update_station(station, request)

    return {'result': 1}


@csrf_exempt
@ajax_request
def update_coords(request, id):
    station = Station.objects.get(id=id)
    station.lt_coord = request.POST['lt']
    station.ln_coord = request.POST['ln']
    station.save()

    return {'result': 1}

@ajax_request
def get_cities(request):
    cities = []
    for city in City.objects.all():
        cities.append({
            'id': city.id,
            'name': city.name,
        })

    return {'cities': cities}
