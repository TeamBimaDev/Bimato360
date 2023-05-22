from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.country.models import BimaCoreCountry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from rest_framework import status
from rest_framework.response import Response
from core.state.models import BimaCoreState
from core.pagination import DefaultPagination


class BimaCoreAddressViewSet(AbstractViewSet):
    queryset = BimaCoreAddress.objects.all()
    serializer_class = BimaCoreAddressSerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def create(self, request):
        addressContentType = ContentType.objects.filter(app_label="core", model="bimacoreaddress").first()
        country_id = request.data.get('country_id')
        state_id = request.data.get('state_id')
        country = get_object_or_404(BimaCoreCountry, id=country_id)
        state = get_object_or_404(BimaCoreState, id=state_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(country=country, state=state, parent_type=addressContentType, parent_id=addressContentType.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data
        country_public_id = request.data.get('country')
        state_public_id = request.data.get('state')
        country = get_object_or_404(BimaCoreCountry, public_id=country_public_id)
        state = get_object_or_404(BimaCoreState, public_id=state_public_id)
        data_to_save['country_id'] = country.id
        data_to_save['state_id'] = state.id
        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaCoreAddress.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
