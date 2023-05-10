from django.urls import path, include

app_name = 'partners'

urlpatterns = [
        path('partners/', include('partners.partners.urls')),
]
