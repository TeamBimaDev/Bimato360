import django_filters
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.apps import apps
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaCoreNotificationTemplate
from .serializers import BimaCoreNotificationTemplateSerializer
from .service import BimaCoreNotificationTemplateService


class BimaCoreNotificationTemplateFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    notification_type = django_filters.UUIDFilter(field_name='notification_type__public_id')
    notification_code = django_filters.CharFilter(field_name='notification_type__code')

    class Meta:
        model = BimaCoreNotificationTemplate
        fields = ['search', 'notification_type', 'notification_code']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(subject__icontains=value) |
            Q(message__icontains=value)
        )


class BimaCoreNotificationTemplateViewSet(AbstractViewSet):
    queryset = BimaCoreNotificationTemplate.objects.all()
    serializer_class = BimaCoreNotificationTemplateSerializer
    filterset_class = BimaCoreNotificationTemplateFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['notification_template.can_read'],
        'create': ['notification_template.can_create'],
        'retrieve': ['notification_template.can_read'],
        'update': ['notification_template.can_update'],
        'partial_update': ['notification_template.can_update'],
        'destroy': ['notification_template.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreNotificationTemplate.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=False, methods=['GET'], url_path="get_template_by_notification_type_code_with_data_rendered")
    def get_template_by_notification_type_code_with_data_rendered(self, request):
        notification_type_code = request.query_params.get('notification_type_code', None)
        document_public_id = request.query_params.get('document_public_id', None)
        if not notification_type_code:
            return Response({"Error": _("Please provide a valid Code")}, status=status.HTTP_400_BAD_REQUEST)

        if not document_public_id:
            return Response({"Error": _("Please provide a valid UUID")}, status=status.HTTP_400_BAD_REQUEST)

        template = BimaCoreNotificationTemplate.objects.filter(notification_type__code=notification_type_code).first()
        if not template:
            return Response({"Error": _("Not template find with the giving code")}, status=status.HTTP_404_NOT_FOUND)

        BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
        sale_document = BimaErpSaleDocument.objects.get_object_by_public_id(document_public_id)
        if not sale_document:
            return Response({"Error": _("Not invoice found with the giving ID")}, status=status.HTTP_404_NOT_FOUND)

        if not sale_document.payment_terms:
            return Response({"Error": _("Invoice does not have any payment terms")}, status=status.HTTP_404_NOT_FOUND)

        subject, message = BimaCoreNotificationTemplateService.get_rendered_template_for_sale_document(sale_document,
                                                                                                       template)
        return Response({'message': message, 'subject': subject})
