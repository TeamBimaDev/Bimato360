from django.urls import path, include

app_name = 'treasury'

urlpatterns = [
        path('payment_method/', include('treasury.payment_method.urls')),
        path('payment_provider/', include('treasury.payment_provider.urls')),
        path('payment_terms/', include('treasury.payment_terms.urls')),
        path('payment_terms_details/', include('treasury.payment_terms_details.urls')),
        path('refund/', include('treasury.refund.urls')),
        path('transaction/', include('treasury.transaction.urls')),
        path('transaction_payment_method/', include('treasury.transaction_payment_method.urls')),
        path('transaction_bank_transfer_detail/',
             include('treasury.transaction_payment_method_bank_transfer_detail.urls')),
        path('transaction_card_transfer_detail/',
             include('treasury.transaction_payment_method_card_transfer_detail.urls')),
        path('transaction_cheque_detail/', include('treasury.transaction_payment_method_cheque_detail.urls')),
]
