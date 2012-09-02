from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import scrapper.admin
import library.admin
import library.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tvdir.views.home', name='home'),
    # url(r'^tvdir/', include('tvdir.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^library/', include(library.urls))
)

