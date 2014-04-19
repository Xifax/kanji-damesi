from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'saiban/', include('saiban.urls')),
    url(r'^$', 'tamesi.views.landing', name='landing'),
)
