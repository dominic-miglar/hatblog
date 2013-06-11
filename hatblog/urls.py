from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

blog_url = 'blog/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hatblog.views.home', name='home'),
    # url(r'^hatblog/', include('hatblog.foo.urls')),

    #url(r'^/$', redirect_to, {'url': '/blog/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls), name='management'),
    url(r'^' + blog_url, include('hatblog.weblog.urls', namespace='hatblog', app_name='weblog')),
    url(r'^$', redirect_to, {'url': blog_url}),
)

