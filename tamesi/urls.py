from django.conf.urls import patterns, include, url

from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'saiban/', include('saiban.urls')),
    url(r'^$', 'tamesi.views.landing', name='landing'),
    url(r'^media/(.*)$', 'django.views.static.serve',
        {'document_root' : settings.MEDIA_ROOT}
    ),
)
