from django.conf.urls import patterns, include, url
import hatblog.weblog.views as views

urlpatterns = patterns('',

    # e.g. /
    url(r'^$', views.home, name='home'),
    
    # e.g. 2013/
    url(r'^(?P<year>\d{4})/$', views.archive, name='year_archive'),
    
    # e.g. 2013/01/
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.archive, name='month_archive'),
    
    # e.g. 2013/01/01/
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.archive, name='day_archive'),
    
    # e.g. 2013/01/01/12341234/this-is-my-slug/
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<id>\d+)/(?P<slug>[0-9a-zA-z\-]+)/(?P<comment>comment)?/$', views.blogentry_detail, name='blogentry_detail'),

    url(r'^impressum/$', views.impressum, name='impressum'),
    url(r'^contact/$', views.contact, name='contact'),
    # url(r'^management/$', views.management, name='management'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'weblog/login.html'}, name='login'),
    url(r'^logout/$', views.logout_page, name='logout'),
)
