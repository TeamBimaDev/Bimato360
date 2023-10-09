import django_filters
from common.enums.position import ContractStatus
from common.enums.position import get_contract_type_choices, get_contract_status_choices
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaHrContract, BimaHrContractAmendment
from .serializers import BimaHrContractSerializer, BimaHrContractAmendmentSerializer


class BimaHrContractFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    employee = django_filters.UUIDFilter(field_name="employee__public_id")
    start_date = django_filters.DateFilter(field_name="start_date")
    end_date = django_filters.DateFilter(field_name="end_date")
    contract_type = django_filters.ChoiceFilter(choices=get_contract_type_choices())
    contract_status = django_filters.ChoiceFilter(choices=get_contract_status_choices())

    class Meta:
        model = BimaHrContract
        fields = ['search', 'employee', 'start_date', 'end_date', 'contract_type', 'contract_status']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(note__icontains=value) |
            Q(job_description__icontains=value)
        )


class BimaHrContractViewSet(AbstractViewSet):
    queryset = BimaHrContract.objects.all()
    serializer_class = BimaHrContractSerializer
    permission_classes = []
    ordering = ["-end_date"]
    filterset_class = BimaHrContractFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['contract.can_read'],
        'create': ['contract.can_create'],
        'retrieve': ['contract.can_read'],
        'update': ['contract.can_update'],
        'partial_update': ['contract.can_update'],
        'destroy': ['contract.can_delete'],
        'suspend_or_terminate': ['contract.can_manage_others_contract'],
    }

    def get_object(self):
        obj = BimaHrContract.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['post'], url_path='add-amendment')
    def add_amendment(self, request, pk=None):
        contract = self.get_object()
        serializer = BimaHrContractAmendmentSerializer(data=request.data, context={'contract': contract})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='get-amendments')
    def get_amendments(self, request, pk=None):
        contract = self.get_object()
        amendments = BimaHrContractAmendment.objects.filter(contract=contract)
        serializer = BimaHrContractAmendmentSerializer(amendments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='update-amendment/(?P<amendment_public_id>[^/.]+)')
    def update_amendment(self, request, pk=None, amendment_public_id=None):
        contract = self.get_object()
        amendment = get_object_or_404(BimaHrContractAmendment, public_id=amendment_public_id, contract=contract)
        serializer = BimaHrContractAmendmentSerializer(amendment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete-amendment/(?P<amendment_public_id>[^/.]+)')
    def delete_amendment(self, request, pk=None, amendment_public_id=None):
        contract = self.get_object()
        amendment = get_object_or_404(BimaHrContractAmendment, public_id=amendment_public_id, contract=contract)
        amendment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list_documents(self, request, *args, **kwargs):
        contract = BimaHrContract.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(contract)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        contract = BimaHrContract.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(contract, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response({
                "id": result.public_id,
                "document_name": result.document_name,
                "description": result.description,
                "date_file": result.date_file,
                "file_type": result.file_type

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_document(self, request, *args, **kwargs):
        contract = BimaHrContract.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=contract.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    @action(detail=False, methods=['get'], url_path='list_contract_types')
    def list_contract_types(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_contract_type_choices()}
        return Response(formatted_response)

    @action(detail=False, methods=['get'], url_path='list_contract_status')
    def list_contract_status(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_contract_status_choices()}
        return Response(formatted_response)

    @action(detail=True, methods=['post'], permission_classes=[], url_path='suspend-or-terminate')
    def suspend_or_terminate(self, request, pk=None):
        contract = self.get_object()

        if not request.user.has_perm('contract.can_manage_others_contract'):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if contract.contract_type != ContractStatus.ACTIVE.name:
            return Response({'detail': 'Contract is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        if contract.reason_stopped is None:
            return Response({'detail': 'Reason stopped is not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        suspend_terminate = request.data.get('suspend_terminate', '').upper()
        if suspend_terminate not in ['SUSPENDED', 'TERMINATED']:
            return Response({'detail': 'Invalid suspend_terminate value.'}, status=status.HTTP_400_BAD_REQUEST)

        contract.status = suspend_terminate
        contract.manager_who_stopped = request.user

        stopped_at = request.data.get('stopped_at')
        if stopped_at:
            try:
                contract.stopped_at = timezone.datetime.strptime(stopped_at, '%Y-%m-%d').date()
            except ValueError:
                return Response({'detail': 'Invalid date format for stopped_at.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            contract.stopped_at = timezone.now().date()

        contract.save()

        serializer = BimaHrContractSerializer(contract)
        return Response(serializer.data)
