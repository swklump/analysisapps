from django.urls import include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.census, name='census'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('parse/', views.parse, name='parse'),
    path('parse/tableids/', views.parse_tableids, name='parse-tableids'),
    path('descriptiveanalysis/', views.descriptiveanalysis, name='descriptiveanalysis'),
    path('advancedanalysis/', views.advancedanalysis, name='advancedanalysis'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)