from django.urls import path, include

app_name = 'core'

urlpatterns = [
    path('currency/', include('core.currency.urls')),
    path('country/', include('core.country.urls')),
    path('state/', include('core.state.urls')),
    path('bank/', include('core.bank.urls')),
    path('contact/', include('core.contact.urls')),
    path('address/', include('core.address.urls')),
    path('document/',include('core.document.urls')),
    path('department/',include('core.department.urls')),
    path('poste/',include('core.poste.urls')),
    path('tags/',include('core.tags.urls')),
]
