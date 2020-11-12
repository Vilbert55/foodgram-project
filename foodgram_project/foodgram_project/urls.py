from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.views.static import serve


urlpatterns = [
    path('about/', include('django.contrib.flatpages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='about-spec'),
    path('api/', include('api.urls')),
    path('', include('mainapp.urls')),

]

handler404 = "foodgram_project.views.page_not_found"  # noqa
handler500 = "foodgram_project.views.server_error"   # noqa

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve,
        {
            'document_root': settings.STATIC_ROOT,
            'show_indexes': settings.DEBUG
        }),
]
