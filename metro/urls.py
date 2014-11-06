import app.urls as app_urls
import backend.urls as backend_urls
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend', include(backend_urls)),
    url(r'^', include(app_urls))
)
