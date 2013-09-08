from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.core.views.homepage',name='homepage'),    
    url(r'^produtos/', include('apps.produto.urls', namespace='produtos')),
    url(r'^carrinho/', include('apps.carrinho.urls', namespace='carrinho')),
    url(r'^meu-perfil/', include('apps.cliente.urls')),    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )
    # staticfiles
    urlpatterns += staticfiles_urlpatterns()


