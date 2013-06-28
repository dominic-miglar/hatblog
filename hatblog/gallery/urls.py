from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from hatblog.gallery.views import ImprintView, ContactView, ImageView, ImageListView, LogoutView

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='images/')),
    url(r'^images/$', ImageListView.as_view(), name='images'),
    url(r'^images/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', ImageView.as_view(), name='image'),
    url(r'^imprint/$', ImprintView.as_view(), name='imprint'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
