from core.abstract.views import AbstractViewSet
from core.bank.models import BimaCoreBank
from core.bank.serializers import BimaCoreBankSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from core.address.serializers import BimaCoreAddressSerializer
from django.shortcuts import get_object_or_404
from core.bank.signals import post_create_bank

from core.address.models import create_single_address, \
    get_addresses_for_parent, \
    BimaCoreAddress


class BimaCoreBankViewSet(AbstractViewSet):
    queryset = BimaCoreBank.objects.all()
    serializer_class = BimaCoreBankSerializer
    permission_classes = []

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        if email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError("Email must be unique.")

        if bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError("BIC must be unique.")

        serializer.save()

    def perform_update(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        instance = serializer.instance

        if email and email != instance.email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError("Email must be unique.")

        if bic and bic != instance.bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError("BIC must be unique.")

        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_bank = get_object_or_404(BimaCoreBank, public_id=serializer.data['public_id'])
        address_data = request.data.get('address_data', [])
        post_create_bank.send(sender=self.__class__, instance=new_bank, address_data=address_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list_addresses(self, request, *args, **kwargs):
        bank = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['public_id'])
        addresses = get_addresses_for_parent(bank)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        bank = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['public_id'])
        saved = create_single_address(request.data, bank)
        if not saved:
            return Response(saved.error, status=saved.status)
        return Response(saved)

    def get_address(self, request, *args, **kwargs):
        partner = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['public_id'])
        address = get_object_or_404(BimaCoreAddress, public_id=self.kwargs['address_public_id'], parent_id=partner.id)
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def get_object(self):
        obj = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
