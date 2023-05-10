from core.abstract.models import AbstractModel
from django.db import models
from partners.models import BimaPartners

class BimaPartnersPayment(AbstractModel):
    partner = models.OneToOneField(BimaPartners)
    payment_conditions_name = models.CharField(max_length=528, blank=False)
    active = models.BooleanField()

    PAYMENT_TYPE_BANK_CARD = 'BANK CARD'
    PAYMENT_TYPE_CREDIT_CARD = 'CREDIT CARD'
    PAYMENT_TYPE_CASH = 'CASH'

    PAYMENT_TYPE_CHOICES = [
        (PAYMENT_TYPE_BANK_CARD, 'BANK CARD'),
        (PAYMENT_TYPE_CREDIT_CARD, 'CREDIT CARD'),
        (PAYMENT_TYPE_CASH, 'CASH'),
    ]
    payment_type = models.CharField(max_length=36, choices=PAYMENT_TYPE_CHOICES)
    days_number = models.IntegerField()
    percentage_discount_allowed = models.FloatField()
    discount_days_number = models.IntegerField()
    penalty = models.FloatField()
    penalty_days = models.IntegerField()

    def __str__(self):
        return f"{self.partner ,self.payment_conditions_name,self.payment_type,self.days_number , self.penalty,self.penalty_days}"

    class Meta:
        ordering = ['payment_conditions_name']
        permissions = []



