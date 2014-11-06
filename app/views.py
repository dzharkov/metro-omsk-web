from annoying.decorators import render_to


@render_to('edit_map.html')
def edit_map(request, id):
    return {'id': id}