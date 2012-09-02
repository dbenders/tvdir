from django.conf.urls import patterns, include, url
from library.views import ChannelListView, ChannelDetailView, ProgramDetailView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tvdir.views.home', name='home'),
    # url(r'^tvdir/', include('tvdir.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^channels/?$', ChannelListView.as_view()),
    url(r'^channels/(?P<pk>\d+)/?$', ChannelDetailView.as_view()),
    url(r'^programs/(?P<pk>\d+)/?$', ProgramDetailView.as_view()),
)

