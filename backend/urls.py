from django.conf.urls import patterns, url

urlpatterns = patterns(
    'backend.views',
    url(r'^/(?P<city_id>\d+)/?$', 'get_card'),
    url(r'^/add_station/?$', 'add_station'),
)