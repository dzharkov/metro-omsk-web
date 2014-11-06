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
    station.next_time = request.POST['next_time']

    if request.POST['next_id']:
        station.next_station = Station.objects.get(id=request.POST['next_id'])

    station.lt_coord = request.POST['lat']
    station.ln_coord = request.POST['lan']
    station.x_coord = 0
    station.y_coord = 0
    station.line = Line.objects.get(id=request.POST['line'])
    station.save()
    return {'result': 1}
