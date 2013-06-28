from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls.static import static
import hatblog.settings as settings

from django.contrib import admin
admin.autodiscover()

blog_url = 'blog/'
gallery_url = 'gallery/'

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^' + blog_url, include('hatblog.weblog.urls', namespace='weblog', app_name='weblog')),
    url(r'^' + gallery_url, include('hatblog.gallery.urls', namespace='gallery', app_name='gallery')),
    url(r'^$', RedirectView.as_view(url=blog_url)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


