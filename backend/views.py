from annoying.decorators import ajax_request
from app.models import City, Station, Line


@ajax_request
def get_card(request, city_id):
    city = City.objects.get(id=city_id)
    return city.as_dict()


@ajax_request
def add_station(request):
    station = Station()

    station.name = request.POST['name']
    station.line = Line.objects.get(id=request.POST['line'])

    if request.POST['next_time']:
        station.next_time = request.POST['next_time']

    station.lt_coord = request.POST['lat']
    station.ln_coord = request.POST['lan']
    station.x_coord = 0
    station.y_coord = 0

    if request.POST['next_id']:
        next_station = Station.objects.get(id=request.POST['next_id'])
        prev_station = next_station.prev_station if hasattr(next_station, 'prev_station') else None
        station.next_station = next_station
    else:
        prev_stations = Station.objects.filter(line=station.line, next_station__isnull=True).all()
        prev_station = None if len(prev_stations) == 0 else prev_stations[0]

    station.save()

    if prev_station is not None:
        prev_station.next_station = station
        prev_station.save()
    return {'result': 1}
