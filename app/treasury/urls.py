from django.urls import path, include

app_name = 'treasury'

urlpatterns = [
    path('cash/', include('treasury.cash.urls')),
    path('bank_account/', include('treasury.bank_account.urls')),
    path('transaction_type/', include('treasury.transaction_type.urls')),
    path('payment_term/', include('treasury.payment_term.urls')),
    # path('payment_method/', include('treasury.payment_method.urls')),
    # path('payment_provider/', include('treasury.payment_provider.urls')),
    # path('refund/', include('treasury.refund.urls')),
    # path('transaction/', include('treasury.transaction.urls')),
    # path('transaction_payment_method/', include('treasury.transaction_payment_method.urls')),
    # path('transaction_bank_transfer_detail/',
    #      include('treasury.transaction_payment_method_bank_transfer_detail.urls')),
    # path('transaction_card_transfer_detail/',
    #      include('treasury.transaction_payment_method_card_transfer_detail.urls')),
    # path('transaction_cheque_detail/', include('treasury.transaction_payment_method_cheque_detail.urls')),
]
