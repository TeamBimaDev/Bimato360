from core.abstract.views import AbstractViewSet
from core.bank.models import BimaCoreBank
from core.bank.serializers import BimaCoreBankSerializer
from core.address.models import BimaCoreAddress
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from core.address.serializers import BimaCoreAddressSerializer
from django.shortcuts import get_object_or_404
from core.pagination import DefaultPagination
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState


class BimaCoreBankViewSet(AbstractViewSet):
    queryset = BimaCoreBank.objects.all()
    serializer_class = BimaCoreBankSerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def create_address(self, address_data, parent_type, parent_id):
        country = get_object_or_404(BimaCoreCountry, public_id=address_data['country'])
        state = get_object_or_404(BimaCoreState, public_id=address_data['state'])

        try:
            address = BimaCoreAddress.objects.create(
                number=address_data['number'],
                street=address_data['street'],
                street2=address_data['street2'],
                zip=address_data['zip'],
                city=address_data['city'],
                state_id=state.id,
                country_id=country.id,
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return address
        except ValueError as expError:
            pass

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank = self.perform_create(serializer)
        bankContentType = ContentType.objects.filter(app_label="core", model="bimacorebank").first()
        if bankContentType:
                bankContentType_id = bankContentType.id

        newBank = get_object_or_404(BimaCoreBank, public_id=serializer.data['public_id'])
        if newBank:
            for address_data in request.data.get('address', []):
                self.create_address(address_data, bankContentType, newBank.id)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list_object(self, request, public_id=None, model=None, serializer=None):
        bankContentType = ContentType.objects.filter(app_label="core", model="bimacorebank").first()
        if bankContentType:
            bank = BimaCoreBank.objects.filter(public_id=public_id)[0]
            objects = model.objects.filter(parent_type_id=bankContentType.id, parent_id=bank.id)
            serialized_data = serializer(objects, many=True)
            return Response(serialized_data.data)
    def list_addresses(self, request, public_id=None):
        model = BimaCoreAddress
        serializer = BimaCoreAddressSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)

    def add_address_for_bank(self, request, public_id=None):
        bank = BimaCoreBank.objects.filter(public_id=public_id).first()
        bankContentType = ContentType.objects.filter(app_label="core", model="bimacorebank").first()
        if not bank:
            return Response({"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND)

        for address_data in request.data.get('address', []):
            self.create_address(address_data, bankContentType, bank.id)

        return Response({"success": "Address(es) added successfully"}, status=status.HTTP_201_CREATED)

    def get_object(self):
        obj = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj
    def update_address_for_bank(self, request, public_id=None, address_id=None):
        bank = get_object_or_404(BimaCoreBank, public_id=public_id)
        bankContentType = ContentType.objects.get(app_label="core", model="bimacorebank")
        address = get_object_or_404(BimaCoreAddress, id=address_id, parent_type=bankContentType, parent_id=bank.id)
        serializer = BimaCoreAddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_address = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

