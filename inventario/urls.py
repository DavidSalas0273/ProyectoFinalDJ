from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # La raíz redirige al login; desde ahí cada rol va a su dashboard
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('', include('core.urls')),
    path('', include('gestion_inventario.urls')),
]
