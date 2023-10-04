from datetime import datetime

from common.enums.vacation import VacationStatus, get_vacation_type_list
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from hr.employee.models import BimaHrEmployee
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
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
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.can_view_all_vacations():
            return queryset
        return queryset.filter(employee__user=self.request.user)

    def perform_create(self, serializer):
        employee_public_id = serializer.validated_data.get("employee_public_id")
        try:
            employee = BimaHrEmployee.objects.get_object_by_public_id(employee_public_id)
        except BimaHrEmployee.DoesNotExist:
            raise ValidationError({"employee": _("Employee with provided id does not exist.")})

        if not employee.position or not employee.position.manager:
            raise ValidationError({"manager": _("Manager for the employee's position is not set.")})

        manager = employee.position.manager

        if self.request.user != employee.user:
            raise PermissionDenied(_("You are not authorized to request a vacation for another employee."))

        serializer.save(manager=manager, employee=employee)

    def perform_update(self, serializer):
        vacation = self.get_object()

        if not (
                self.request.user == vacation.employee.user
                or self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            raise PermissionDenied(_("You are not authorized to perform this action."))

        if self.request.user == vacation.employee:
            if vacation.status != VacationStatus.PENDING.value:
                raise PermissionDenied(_("You can only update a vacation if its status is PENDING."))
            serializer.save()
            return

        is_status_changing = serializer.validated_data.get('status') != vacation.status

        if (
                self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            if serializer.validated_data.get('status') not in [VacationStatus.APPROVED.value,
                                                               VacationStatus.REFUSED.value]:
                raise PermissionDenied(_("As a manager, you can only approve or refuse a vacation."))

            with transaction.atomic():
                if serializer.validated_data.get('status') == VacationStatus.APPROVED.value:
                    is_valid, requested_days = is_vacation_request_valid(vacation)
                    if not is_valid:
                        raise ValidationError({
                            'error': _('Requested vacation days exceed available balance by {} days.').format(
                                requested_days - vacation.employee.balance_vacation
                            )
                        })

                try:
                    if is_status_changing:
                        vacation.status_change_date = datetime.now()
                        vacation.save(update_fields=['status_change_date'])
                    update_vacation_status(vacation, serializer.validated_data.get('status'),
                                           serializer.validated_data.get('reason_refused'), save=False)
                except ValueError:
                    raise ValidationError({'error': _('Invalid data')})
                serializer.save()

    @action(detail=True, methods=['get'], url_path='get_vacation_balance')
    def get_vacation_balance(self, request, pk=None):
        vacation = self.get_object()
        employee = vacation.employee
        balance = {
            'balance_vacation': employee.balance_vacation,
            'virtual_balance_vacation': employee.virtual_balance_vacation
        }
        return Response(balance)

    @action(detail=False, methods=['get'], url_path='see_affected_vacation')
    def see_affected_vacation(self, request):
        if self.can_view_all_vacations():
            queryset = BimaHrVacation.objects.all()
        else:
            queryset = BimaHrVacation.objects.filter(manager__user=self.request.user)

        filtered_queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list_vacation_type')
    def list_vacation_type(self, request, *args, **kwargs):
        return Response(get_vacation_type_list())

    def get_object(self):
        obj = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def can_view_all_vacations(self):
        return self.request.user.has_perm('vacation.can_view_all_vacation')
