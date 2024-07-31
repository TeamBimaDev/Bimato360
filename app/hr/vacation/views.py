<<<<<<< HEAD
from datetime import datetime
from io import BytesIO

from common.enums.vacation import VacationStatus, get_vacation_type_list, get_vacation_status_list
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.pagination import DefaultPagination
from core.abstract.views import AbstractViewSet
from core.document.models import get_documents_for_parent_entity, BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hr.employee.models import BimaHrEmployee
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .filters import BimaHrVacationFilter
from .models import BimaHrVacation
from .serializers import BimaHrVacationSerializer
from .service import is_vacation_request_valid, update_vacation_status, calculate_vacation_balances, \
    BimaHrVacationExportService, EmployeeExporter, BimaVacationNotificationService


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
        'export_xls': ['vacation.can_view_all_vacation'],
        'export_csv': ['vacation.can_view_all_vacation'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.can_view_all_vacations():
            return queryset
        return queryset.filter(employee__user=self.request.user)

    def perform_create(self, serializer):
        employee = serializer.validated_data.get("employee")
        if not employee.position or not employee.position.manager:
            raise ValidationError({"manager": _("Manager for the employee's position is not set.")})

        manager = employee.position.manager

        if self.request.user != employee.user:
            raise PermissionDenied(_("You are not authorized to request a vacation for another employee."))

        vacation = serializer.save(manager=manager, employee=employee)
        BimaVacationNotificationService.send_notification_request_vacation(vacation)

    def perform_update(self, serializer):
        vacation = self.get_object()

        if not (
                self.request.user == vacation.employee.user
                or self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            raise PermissionDenied(_("You are not authorized to perform this action."))

        if self.request.user == vacation.employee.user:
            if vacation.status != VacationStatus.PENDING.name:
                raise PermissionDenied(_("You can only update a vacation if its status is PENDING."))
            serializer.save()
            return

        is_status_changing = serializer.validated_data.get('status') != vacation.status

        if (
                self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            if serializer.validated_data.get('status') not in [VacationStatus.APPROVED.name,
                                                               VacationStatus.REFUSED.name]:
                raise PermissionDenied(_("As a manager, you can only approve or refuse a vacation."))

            with transaction.atomic():
                if serializer.validated_data.get('status') == VacationStatus.APPROVED.name:
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

        paginator = DefaultPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list_vacation_type')
    def list_vacation_type(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_vacation_type_list()}
        return Response(formatted_response)

    @action(detail=False, methods=['get'], url_path='list_vacation_status')
    def list_vacation_status(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_vacation_status_list()}
        return Response(formatted_response)

    @action(detail=False, methods=['GET'], url_path='calculate_vacation_balance')
    def calculate_vacation_balance(self, request):
        balance_array = []
        with transaction.atomic():
            for employee in BimaHrEmployee.objects.all():
                employee_old_vacation_balance = employee.balance_vacation
                employee_old_virtual_vacation_balance = employee.virtual_balance_vacation
                calculate_vacation_balances(employee)
                employee_new_vacation_balance = employee.balance_vacation
                employee_new_virtual_vacation_balance = employee.virtual_balance_vacation
                balance_array.append(
                    {"employee_public_id": employee.public_id,
                     "employee_full_name": employee.full_name,
                     "old_vacation_balance": employee_old_vacation_balance,
                     "new_vacation_balance": employee_new_vacation_balance,
                     "old_virtual_vacation_balance": employee_old_virtual_vacation_balance,
                     "new_virtual_vacation_balance": employee_new_virtual_vacation_balance
                     })

        return Response(balance_array)

    @action(detail=False, methods=["GET"], url_path="export_csv")
    def export_csv(self, request):
        queryset = None
        if self.can_view_all_vacations():
            queryset = BimaHrVacation.objects.all()
        else:
            queryset = BimaHrVacation.objects.filter(manager__user=self.request.user)

        filtered_qs = BimaHrVacationFilter(request.GET, queryset=queryset).qs
        service = BimaHrVacationExportService(filtered_qs)
        csv_data = service.export_to_csv()

        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=vacations_export.csv"
        return response

    @action(detail=False, methods=["GET"], url_path="export_xls")
    def export_xls(self, request):
        filtered_qs = BimaHrVacationFilter(request.GET, queryset=self.get_queryset()).qs
        service = BimaHrVacationExportService(filtered_qs)
        excel_data = service.export_to_excel()

        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=vacations_export.xlsx"
        return response

    @action(detail=False, methods=["GET"], url_path="export_employee_vacation")
    def export_employee_vacation(self, request):
        employee_public_id = request.query_params.get('employee_public_id')
        employee = None
        if employee_public_id:
            try:
                employee = BimaHrEmployee.objects.get_object_by_public_id(employee_public_id)
            except BimaHrEmployee.DoesNotExist:
                pass  # Handle employee not found

        exporter = EmployeeExporter(employee)
        exporter.export()

        buffer = BytesIO()
        excel_data = exporter.save(buffer)

        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=employee_vacation_export.xlsx"
        return response

    @action(detail=True, methods=['post'], url_path='approve_refuse_vacation')
    def approve_refuse_vacation(self, request, pk=None):
        vacation = self.get_object()
        self.check_user_permissions(vacation)

        status = request.data.get('status').upper()
        reason_refused = request.data.get('reason_refused', None)
        is_status_changing = status != vacation.status

        if status not in [VacationStatus.APPROVED.name, VacationStatus.REFUSED.name]:
            raise ValidationError({"status": _("Invalid status value.")})

        with transaction.atomic():
            if is_status_changing:
                vacation = update_vacation_status(vacation, status, reason_refused, save=False)
            vacation.save()

        BimaVacationNotificationService.send_approval_refusal_notification(vacation)

        serializer = self.get_serializer(vacation)
        return Response(serializer.data)

    def list_documents(self, request, *args, **kwargs):
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(vacation)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(vacation, document_data)
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
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=vacation.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def check_user_permissions(self, vacation):
        user = self.request.user
        if not (
                user == vacation.manager.user
                or user.has_perm('hr.vacation.can_manage_other_vacation')
        ):
            raise PermissionDenied(_("You are not authorized to perform this action."))

    def get_object(self):
        obj = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def can_view_all_vacations(self):
        return self.request.user.has_perm('hr.vacation.can_view_all_vacation')
=======
from datetime import datetime
from io import BytesIO

from common.enums.vacation import VacationStatus, get_vacation_type_list, get_vacation_status_list
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.pagination import DefaultPagination
from core.abstract.views import AbstractViewSet
from core.document.models import get_documents_for_parent_entity, BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hr.employee.models import BimaHrEmployee
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .filters import BimaHrVacationFilter
from .models import BimaHrVacation
from .serializers import BimaHrVacationSerializer
from .service import is_vacation_request_valid, update_vacation_status, calculate_vacation_balances, \
    BimaHrVacationExportService, EmployeeExporter, BimaVacationNotificationService


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
        'export_xls': ['vacation.can_view_all_vacation'],
        'export_csv': ['vacation.can_view_all_vacation'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.can_view_all_vacations():
            return queryset
        return queryset.filter(employee__user=self.request.user)

    def perform_create(self, serializer):
        employee = serializer.validated_data.get("employee")
        if not employee.position or not employee.position.manager:
            raise ValidationError({"manager": _("Manager for the employee's position is not set.")})

        manager = employee.position.manager

        if self.request.user != employee.user:
            raise PermissionDenied(_("You are not authorized to request a vacation for another employee."))

        vacation = serializer.save(manager=manager, employee=employee)
        BimaVacationNotificationService.send_notification_request_vacation(vacation)

    def perform_update(self, serializer):
        vacation = self.get_object()

        if not (
                self.request.user == vacation.employee.user
                or self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            raise PermissionDenied(_("You are not authorized to perform this action."))

        if self.request.user == vacation.employee.user:
            if vacation.status != VacationStatus.PENDING.name:
                raise PermissionDenied(_("You can only update a vacation if its status is PENDING."))
            serializer.save()
            return

        is_status_changing = serializer.validated_data.get('status') != vacation.status

        if (
                self.request.user == vacation.manager.user
                or self.request.user.has_perm('vacation.can_manage_other_vacation')
        ):
            if serializer.validated_data.get('status') not in [VacationStatus.APPROVED.name,
                                                               VacationStatus.REFUSED.name]:
                raise PermissionDenied(_("As a manager, you can only approve or refuse a vacation."))

            with transaction.atomic():
                if serializer.validated_data.get('status') == VacationStatus.APPROVED.name:
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

        paginator = DefaultPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list_vacation_type')
    def list_vacation_type(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_vacation_type_list()}
        return Response(formatted_response)

    @action(detail=False, methods=['get'], url_path='list_vacation_status')
    def list_vacation_status(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_vacation_status_list()}
        return Response(formatted_response)

    @action(detail=False, methods=['GET'], url_path='calculate_vacation_balance')
    def calculate_vacation_balance(self, request):
        balance_array = []
        with transaction.atomic():
            for employee in BimaHrEmployee.objects.all():
                employee_old_vacation_balance = employee.balance_vacation
                employee_old_virtual_vacation_balance = employee.virtual_balance_vacation
                calculate_vacation_balances(employee)
                employee_new_vacation_balance = employee.balance_vacation
                employee_new_virtual_vacation_balance = employee.virtual_balance_vacation
                balance_array.append(
                    {"employee_public_id": employee.public_id,
                     "employee_full_name": employee.full_name,
                     "old_vacation_balance": employee_old_vacation_balance,
                     "new_vacation_balance": employee_new_vacation_balance,
                     "old_virtual_vacation_balance": employee_old_virtual_vacation_balance,
                     "new_virtual_vacation_balance": employee_new_virtual_vacation_balance
                     })

        return Response(balance_array)

    @action(detail=False, methods=["GET"], url_path="export_csv")
    def export_csv(self, request):
        queryset = None
        if self.can_view_all_vacations():
            queryset = BimaHrVacation.objects.all()
        else:
            queryset = BimaHrVacation.objects.filter(manager__user=self.request.user)

        filtered_qs = BimaHrVacationFilter(request.GET, queryset=queryset).qs
        service = BimaHrVacationExportService(filtered_qs)
        csv_data = service.export_to_csv()

        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=vacations_export.csv"
        return response

    @action(detail=False, methods=["GET"], url_path="export_xls")
    def export_xls(self, request):
        filtered_qs = BimaHrVacationFilter(request.GET, queryset=self.get_queryset()).qs
        service = BimaHrVacationExportService(filtered_qs)
        excel_data = service.export_to_excel()

        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=vacations_export.xlsx"
        return response

    @action(detail=False, methods=["GET"], url_path="export_employee_vacation")
    def export_employee_vacation(self, request):
        employee_public_id = request.query_params.get('employee_public_id')
        employee = None
        if employee_public_id:
            try:
                employee = BimaHrEmployee.objects.get_object_by_public_id(employee_public_id)
            except BimaHrEmployee.DoesNotExist:
                pass  # Handle employee not found

        exporter = EmployeeExporter(employee)
        exporter.export()

        buffer = BytesIO()
        excel_data = exporter.save(buffer)

        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=employee_vacation_export.xlsx"
        return response

    @action(detail=True, methods=['post'], url_path='approve_refuse_vacation')
    def approve_refuse_vacation(self, request, pk=None):
        vacation = self.get_object()
        self.check_user_permissions(vacation)

        status = request.data.get('status').upper()
        reason_refused = request.data.get('reason_refused', None)
        is_status_changing = status != vacation.status

        if status not in [VacationStatus.APPROVED.name, VacationStatus.REFUSED.name]:
            raise ValidationError({"status": _("Invalid status value.")})

        with transaction.atomic():
            if is_status_changing:
                vacation = update_vacation_status(vacation, status, reason_refused, save=False)
            vacation.save()

        BimaVacationNotificationService.send_approval_refusal_notification(vacation)

        serializer = self.get_serializer(vacation)
        return Response(serializer.data)

    def list_documents(self, request, *args, **kwargs):
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(vacation)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(vacation, document_data)
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
        vacation = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=vacation.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def check_user_permissions(self, vacation):
        user = self.request.user
        if not (
                user == vacation.manager.user
                or user.has_perm('hr.vacation.can_manage_other_vacation')
        ):
            raise PermissionDenied(_("You are not authorized to perform this action."))

    def get_object(self):
        obj = BimaHrVacation.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def can_view_all_vacations(self):
        return self.request.user.has_perm('hr.vacation.can_view_all_vacation')
>>>>>>> origin/ma-branch
