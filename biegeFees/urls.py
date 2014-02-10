from django.conf.urls import patterns, include, url

from django.conf import settings

from model_report import report
report.autodiscover()

from django.contrib import admin

admin.autodiscover()



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'biegeFees.views.home', name='home'),
    # url(r'^biegeFees/', include('biegeFees.foo.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^report/', include('model_report.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^beige/', include('biegeFeesApp.urls')),
    url(r'^themes/', include('themes.urls')),
    #url(r'^beigefees/', include('biegeFees.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT,}),
)
