from annoying.decorators import ajax_request
from app.models import City, Station, Line, Transition
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
            'lt_coord': city.lt_coord,
            'ln_coord': city.ln_coord
        })

    return {'cities': cities}

@csrf_exempt
@ajax_request
def delete_station(request, id):
    station = Station.objects.get(id=id)
    prev = station.prev_station if hasattr(station, 'prev_station') else None
    next = station.next_station

    station.delete()

    if prev is not None:
        prev.next_station = next
        prev.save()

    return {'result': 1}

@csrf_exempt
@ajax_request
def create_transition(request):
    station1 = Station.objects.get(id=request.POST['id1'])
    station2 = Station.objects.get(id=request.POST['id2'])

    transition = Transition()
    transition.time = 300
    transition.from_station = station1
    transition.to_station = station2
    transition.save()

    transition = Transition()
    transition.time = 300
    transition.from_station = station2
    transition.to_station = station1
    transition.save()

    return {'result': 1}
