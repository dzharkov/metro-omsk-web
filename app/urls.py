from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^(?P<id>\d+)/?$', 'edit_map'),
)