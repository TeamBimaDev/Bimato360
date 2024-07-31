<<<<<<< HEAD
from django.urls import path, include

app_name = 'treasury'

urlpatterns = [
    path('cash/', include('treasury.cash.urls')),
    path('bank_account/', include('treasury.bank_account.urls')),
    path('transaction_type/', include('treasury.transaction_type.urls')),
    path('payment_term/', include('treasury.payment_term.urls')),
    path('transaction/', include('treasury.transaction.urls')),
    path('payment_method/', include('treasury.payment_method.urls')),
]
=======
from django.urls import path, include

app_name = 'treasury'

urlpatterns = [
    path('cash/', include('treasury.cash.urls')),
    path('bank_account/', include('treasury.bank_account.urls')),
    path('transaction_type/', include('treasury.transaction_type.urls')),
    path('payment_term/', include('treasury.payment_term.urls')),
    path('transaction/', include('treasury.transaction.urls')),
    path('payment_method/', include('treasury.payment_method.urls')),
]
>>>>>>> origin/ma-branch
