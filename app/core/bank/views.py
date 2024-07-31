<<<<<<< HEAD
import django_filters

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions.action_base_permission import ActionBasedPermission
from core.address.serializers import BimaCoreAddressSerializer
from core.abstract.views import AbstractViewSet
from core.address.models import create_single_address, \
    get_addresses_for_parent, \
    BimaCoreAddress

from .models import BimaCoreBank
from .serializers import BimaCoreBankSerializer
from .signals import post_create_bank


class BankFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.ChoiceFilter(choices=[('True', 'True'), ('False', 'False'), ('all', 'all')],
                                         method='filter_active')

    class Meta:
        model = BimaCoreBank
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all':
            return queryset
        else:
            return queryset.filter(active=(value == 'True'))


class BimaCoreBankViewSet(AbstractViewSet):
    queryset = BimaCoreBank.objects.all()
    serializer_class = BimaCoreBankSerializer
    filterset_class = BankFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'email', 'bic']

    action_permissions = {
        'list': ['bank.can_read'],
        'create': ['bank.can_create'],
        'retrieve': ['bank.can_read'],
        'update': ['bank.can_update'],
        'partial_update': ['bank.can_update'],
        'destroy': ['bank.can_delete'],
    }

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        if email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError(_("Email must be unique."))

        if bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError(_("BIC must be unique."))

        serializer.save()

    def perform_update(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        instance = serializer.instance

        if email and email != instance.email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError(_("Email must be unique."))

        if bic and bic != instance.bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError(_("BIC must be unique."))

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
        response = create_single_address(request.data, bank)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        bank = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['public_id'])
        address = get_object_or_404(BimaCoreAddress, public_id=self.kwargs['address_public_id'], parent_id=bank.id)
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def get_object(self):
        obj = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
=======
import django_filters

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions.action_base_permission import ActionBasedPermission
from core.address.serializers import BimaCoreAddressSerializer
from core.abstract.views import AbstractViewSet
from core.address.models import create_single_address, \
    get_addresses_for_parent, \
    BimaCoreAddress

from .models import BimaCoreBank
from .serializers import BimaCoreBankSerializer
from .signals import post_create_bank


class BankFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.ChoiceFilter(choices=[('True', 'True'), ('False', 'False'), ('all', 'all')],
                                         method='filter_active')

    class Meta:
        model = BimaCoreBank
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all':
            return queryset
        else:
            return queryset.filter(active=(value == 'True'))


class BimaCoreBankViewSet(AbstractViewSet):
    queryset = BimaCoreBank.objects.all()
    serializer_class = BimaCoreBankSerializer
    filterset_class = BankFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'email', 'bic']

    action_permissions = {
        'list': ['bank.can_read'],
        'create': ['bank.can_create'],
        'retrieve': ['bank.can_read'],
        'update': ['bank.can_update'],
        'partial_update': ['bank.can_update'],
        'destroy': ['bank.can_delete'],
    }

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        if email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError(_("Email must be unique."))

        if bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError(_("BIC must be unique."))

        serializer.save()

    def perform_update(self, serializer):
        email = self.request.data.get('email')
        bic = self.request.data.get('bic')

        instance = serializer.instance

        if email and email != instance.email and BimaCoreBank.objects.filter(email=email).exists():
            raise ValidationError(_("Email must be unique."))

        if bic and bic != instance.bic and BimaCoreBank.objects.filter(bic=bic).exists():
            raise ValidationError(_("BIC must be unique."))

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
        response = create_single_address(request.data, bank)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        bank = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['public_id'])
        address = get_object_or_404(BimaCoreAddress, public_id=self.kwargs['address_public_id'], parent_id=bank.id)
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def get_object(self):
        obj = BimaCoreBank.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
>>>>>>> origin/ma-branch
