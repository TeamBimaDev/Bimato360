from rest_framework import status
from rest_framework.response import Response
from core.abstract.views import AbstractViewSet
from core.country.models import BimaCoreCountry
from core.country.serializers import BimaCoreCountrySerializer
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from core.currency.models import BimaCoreCurrency
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer
from core.pagination import DefaultPagination


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.select_related('currency').all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def create(self, request):
        currency_public_id = request.data.get('currency')
        currency = get_object_or_404(BimaCoreCurrency, public_id=currency_public_id)
        data_to_save = request.data
        data_to_save['currency_id'] = currency.id
        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data.copy()
        currency_public_id = data_to_save.get('currency')
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

    def get_state_by_country(self, request, public_id=None):
        country = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['public_id'])
        states = BimaCoreState.objects.filter(country=country)
        serializer = BimaCoreStateSerializer(states, many=True)
        return Response(serializer.data)
