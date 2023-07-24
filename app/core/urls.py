from django.urls import path, include

from .views import CoreView

app_name = 'core'

urlpatterns = [
    path('currency/', include('core.currency.urls')),
    path('country/', include('core.country.urls')),
    path('state/', include('core.state.urls')),
    path('bank/', include('core.bank.urls')),
    path('cash/', include('core.cash.urls')),
    path('contact/', include('core.contact.urls')),
    path('address/', include('core.address.urls')),
    path('document/', include('core.document.urls')),
    path('department/', include('core.department.urls')),
    path('post/', include('core.post.urls')),
    path('tag/', include('core.tag.urls')),
    path('entity_tag/', include('core.entity_tag.urls')),
    path('source/', include('core.source.urls')),
    path('utils/<str:action>/', CoreView.as_view(), name='utility'),
]
