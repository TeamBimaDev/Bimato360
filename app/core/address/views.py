from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.country.models import BimaCoreCountry
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from core.state.models import BimaCoreState
from core.pagination import DefaultPagination


def get_country_and_state_from_request(data):
    country = get_object_or_404(BimaCoreCountry, public_id=data.get('country'))
    state = get_object_or_404(BimaCoreState, public_id=data.get('state'))
    data['country_id'] = country.id
    data['state_id'] = state.id
    return data


class BimaCoreAddressViewSet(AbstractViewSet):
    queryset = BimaCoreAddress.objects.select_related('state', 'country').all()
    serializer_class = BimaCoreAddressSerializer
    permission_classes = []
    pagination_class = DefaultPagination

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data_to_save = request.data.copy()
            data_to_save = get_country_and_state_from_request(data_to_save)
            serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            queryset = self.filter_queryset(self.get_queryset())
            if queryset._prefetch_related_lookups:
                instance._prefetched_objects_cache = {}
                prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except BimaCoreAddress.DoesNotExist:
            return Response('Item was not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self):
        obj = BimaCoreAddress.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
