from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.census, name='WebApp-census'),
    path('parse/', views.parse, name='WebApp-census-parse'),
    path('parse/tableids/', views.parse_tableids, name='parse-tableids'),
    path('descriptive-analysis/', views.descriptiveanalysis, name='descriptiveanalysis'),
    path('advanced-analysis/', views.advancedanalysis, name='advancedanalysis'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)