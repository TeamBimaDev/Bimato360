from core.abstract.views import AbstractViewSet
from core.state.models import BimaCoreState
from core.permissions import IsAdminOrReadOnly
from core.state.serializers import BimaCoreStateSerializer
from rest_framework import status
from rest_framework.response import Response
from core.country.models import BimaCoreCountry
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from core.pagination import DefaultPagination


class BimaCoreStateViewSet(AbstractViewSet):
    queryset = BimaCoreState.objects.all()
    serializer_class = BimaCoreStateSerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def create(self, request):
        country_public_id = request.data.get(' country')
        country = get_object_or_404(BimaCoreCountry, public_id=country_public_id)
        data_to_save = request.data
        data_to_save[' country_id'] = country.id
        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data.copy()
        country_public_id = data_to_save.get('country')
        country = get_object_or_404(BimaCoreCountry, public_id=country_public_id)
        data_to_save['country_id'] = country.id
        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaCoreState.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
