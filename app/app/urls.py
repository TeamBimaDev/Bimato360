from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/user/', include('user.urls')),
    path('api/core/', include('core.urls')),
    path('api/company/', include('company.urls')),
    path('api/erp/', include('erp.urls')),
    path('api/analysis/', include('analysis.urls')),
    path('api/treasury/', include('treasury.urls')),
    path('api/hr/', include('hr.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
