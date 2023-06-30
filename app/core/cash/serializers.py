from rest_framework import serializers
from .models import BimaCoreCash
from core.abstract.serializers import AbstractSerializer
class BimaCoreCashSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreCash
        fields = '__all__'
