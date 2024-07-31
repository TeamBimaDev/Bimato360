<<<<<<< HEAD
from django.urls import path, include

from .views import CoreView

app_name = 'core'

urlpatterns = [
    path('currency/', include('core.currency.urls')),
    path('country/', include('core.country.urls')),
    path('state/', include('core.state.urls')),
    path('bank/', include('core.bank.urls')),
    path('contact/', include('core.contact.urls')),
    path('address/', include('core.address.urls')),
    path('document/', include('core.document.urls')),
    path('department/', include('core.department.urls')),
    path('tag/', include('core.tag.urls')),
    path('entity_tag/', include('core.entity_tag.urls')),
    path('source/', include('core.source.urls')),
    path('notification/', include('core.notification.urls')),
    path('notification_template/', include('core.notification_template.urls')),
    path('notification_type/', include('core.notification_type.urls')),
    path('utils/<str:action>/', CoreView.as_view(), name='utility'),
]
=======
from django.urls import path, include

from .views import CoreView

app_name = 'core'

urlpatterns = [
    path('currency/', include('core.currency.urls')),
    path('country/', include('core.country.urls')),
    path('state/', include('core.state.urls')),
    path('bank/', include('core.bank.urls')),
    path('contact/', include('core.contact.urls')),
    path('address/', include('core.address.urls')),
    path('document/', include('core.document.urls')),
    path('department/', include('core.department.urls')),
    path('tag/', include('core.tag.urls')),
    path('entity_tag/', include('core.entity_tag.urls')),
    path('source/', include('core.source.urls')),
    path('notification/', include('core.notification.urls')),
    path('notification_template/', include('core.notification_template.urls')),
    path('notification_type/', include('core.notification_type.urls')),
    path('utils/<str:action>/', CoreView.as_view(), name='utility'),
]
>>>>>>> origin/ma-branch
