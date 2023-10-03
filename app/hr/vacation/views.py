from common.enums.vacation import VacationStatus
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from hr.employee.models import BimaHrEmployee
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .filters import BimaHrVacationFilter
from .models import BimaHrVacation
from .serializers import BimaHrVacationSerializer
from .service import is_vacation_request_valid, update_vacation_status


class BimaHrVacationViewSet(AbstractViewSet):
    queryset = BimaHrVacation.objects.all()
    serializer_class = BimaHrVacationSerializer
    filterset_class = BimaHrVacationFilter
    ordering = ["-date_start"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['vacation.can_read'],
        'create': ['vacation.can_create'],
        'retrieve': ['vacation.can_read'],
        'update': ['vacation.can_update'],
        'partial_update': ['vacation.can_update'],
        'destroy': ['vacation.can_delete'],
        'manage_vacation': ['vacation.can_manage_other_vacation'],
    }

    @action(detail=False, methods=['post'])
    def request_vacation(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='manage_vacation')
    def manage_vacation(self, request, pk=None):
        vacation = self.get_object()

        manager_public_id = str(request.user.public_id)
        if str(vacation.manager.public_id) != manager_public_id:
            raise PermissionDenied(_("You are not authorized to manage this vacation."))

        status_update = request.data.get('status')
        reason_refused = request.data.get('reason_refused', None)

        with transaction.atomic():
            if status_update == VacationStatus.APPROVED.value:
                is_valid, requested_days = is_vacation_request_valid(vacation)
                if not is_valid:
                    return Response({
                        'error': _('Requested vacation days exceed available balance by {} days.').format(
                            requested_days - vacation.employee.balance_vacation)},
                        status=status.HTTP_400_BAD_REQUEST)
            try:
                updated_vacation = update_vacation_status(vacation, status_update, reason_refused)
            except ValueError:
                return Response({'error': _('Invalid data')}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(updated_vacation).data)

    @action(detail=False, methods=['get'])
    def employee_vacations(self, request):
        employee_id = request.query_params.get('employee_id')
        try:
            employee = BimaHrEmployee.objects.get(public_id=employee_id)
        except BimaHrEmployee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        vacations = self.get_queryset().filter(employee=employee)
        serializer = self.get_serializer(vacations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='get_vacation_balance')
    def get_vacation_balance(self, request, pk=None):
        vacation = self.get_object()
        employee = vacation.employee
        balance = {
            'balance_vacation': employee.balance_vacation,
            'virtual_balance_vacation': employee.virtual_balance_vacation
        }
        return Response(balance)

    def get_object(self):
        obj = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
