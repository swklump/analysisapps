from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.traffic, name='traffic'),
    path('aktrafficdata/', views.aktrafficdata, name='aktrafficdata'),
    path('ihsdm/', views.ihsdm, name='ihsdm'),
    path('tam/', views.tam, name='tam'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)