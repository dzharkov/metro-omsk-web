from annoying.decorators import render_to


@render_to('edit_map.html')
def edit_map(request, city_id):
    return {'id': city_id}


@render_to('index.html')
def view_city(request, city_id=None):
    return {}
