from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.views',
    url(r'^(?P<city_id>\d+)/edit/?$', 'edit_map'),
    url(r'^(?P<city_id>\d+)/?', 'view_city'),
    url(r'^.*', 'view_city')
)