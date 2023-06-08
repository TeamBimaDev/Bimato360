from rest_framework.response import Response
from core.abstract.views import AbstractViewSet
from core.country.models import BimaCoreCountry
from core.country.serializers import BimaCoreCountrySerializer
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.select_related('currency').all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def get_state_by_country(self, request, public_id=None):
        country = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['public_id'])
        states = BimaCoreState.objects.filter(country=country)
        serializer = BimaCoreStateSerializer(states, many=True)
        return Response(serializer.data)
