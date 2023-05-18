from rest_framework import status
from rest_framework.response import Response
from core.abstract.views import AbstractViewSet
from core.country.models import BimaCoreCountry
from core.permissions import IsAdminOrReadOnly
from core.country.serializers import BimaCoreCountrySerializer
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from core.currency.models import BimaCoreCurrency


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []

    def create(self, request):
        currency_id = request.data.get('currency_id')
        currency = get_object_or_404(BimaCoreCurrency, id=currency_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(currency=currency)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data
        currency_public_id = request.data.get('currency')
        currency = get_object_or_404(BimaCoreCurrency, public_id=currency_public_id)
        data_to_save['currency_id'] = currency.id
        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
