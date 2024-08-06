
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.notification_type.models import BimaCoreNotificationType
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filter import BimaCoreNotificationFilter
from .models import BimaCoreNotification
from .serializers import BimaCoreNotificationSerializer
from .service import BimaErpNotificationService


class BimaCoreNotificationViewSet(AbstractViewSet):
    queryset = BimaCoreNotification.objects.all()
    serializer_class = BimaCoreNotificationSerializer
    filterset_class = BimaCoreNotificationFilter
    ordering = ["-date_sent"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['notification.can_read'],
        'retrieve': ['notification_type.can_read'],
    }

    def get_object(self):
        obj = BimaCoreNotification.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['POST'])
    def save_notification_data(self, request):
        data = request.data
        receivers = data.get('receivers', [])
        subject = data.get('subject', '')
        message = data.get('message', '')
        app_name = data.get('app_name', '')
        model_name = data.get('model_name', '')
        parent_id = data.get('parent_id', '')
        attachments = data.get('attachments', [])
        notification_type_public_id = data.get('notification_type_public_id', '')
        notification_type = BimaCoreNotificationType.objects.get(public_id=notification_type_public_id)
        sender = request.user if request.user.is_authenticated else None

        notification = BimaErpNotificationService.save_notification(receivers, subject, message, attachments,
                                                                    notification_type.id, sender, app_name, model_name,
                                                                    parent_id)

        serializer = BimaCoreNotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def read_notification_by_id(self, request):
        public_id = request.query_params.get('public_id', None)

        if not public_id:
            return Response({'error': 'public_id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            notification = BimaCoreNotification.objects.get(public_id=public_id)
        except BimaCoreNotification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)

        attachments = notification.attachments or []
        receivers_email = notification.receivers_email or []

        notification.attachments = attachments
        notification.receivers_email = receivers_email

        serializer = BimaCoreNotificationSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path="sent_payment_late_notification_sale_document")
    def sent_payment_late_notification_sale_document(self, request):
        sale_document_public_id = request.data.get('sale_document_public_id', None)
        message = request.data.get('message', None)
        subject = request.data.get('subject', None)
        if not sale_document_public_id:
            return Response({"Error": _("Please provide a valid UUID")}, status=status.HTTP_400_BAD_REQUEST)

        BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
        sale_document = BimaErpSaleDocument.objects.get_object_by_public_id(sale_document_public_id)
        if not sale_document:
            return Response({"Error": _("Unable to find item")}, status=status.HTTP_400_BAD_REQUEST)

        if not sale_document.is_confirmed_and_invoice:
            return Response({"Error": _("Only Confirmed Invoice are allowed")}, status=status.HTTP_404_NOT_FOUND)

        if not sale_document.is_payment_late:
            return Response({"Error": _("The payment is not late for this invoice")},
                            status=status.HTTP_400_BAD_REQUEST)

        if sale_document.is_paid:
            return Response({"Error": _("The invoice is already paid")}, status=status.HTTP_404_NOT_FOUND)

        if not sale_document.payment_terms:
            return Response({"Error": _("Invoice does not have any payment terms")}, status=status.HTTP_404_NOT_FOUND)

        BimaErpNotificationService.send_notification_payment_sale_document_based_on_payment_term_type(
            sale_document, days_difference=1, template_code='NOTIFICATION_PAYMENT_LATE', message=message,
            subject=subject, send_instantly=True)
        return Response(_("NOTIFICATION_SALE_DOCUMENT_PAYMENT_LATE_SENT_SUCCESSFUL"))

    @action(detail=False, methods=['POST'], url_path="sent_payment_reminder_notification_sale_document")
    def sent_payment_reminder_notification_sale_document(self, request):
        sale_document_public_id = request.data.get('sale_document_public_id', None)
        message = request.data.get('message', None)
        subject = request.data.get('subject', None)

        if not sale_document_public_id:
            return Response({"Error": _("Please provide a valid UUID")}, status=status.HTTP_400_BAD_REQUEST)

        BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
        sale_document = BimaErpSaleDocument.objects.get_object_by_public_id(sale_document_public_id)
        if not sale_document:
            return Response({"Error": _("Unable to find item")}, status=status.HTTP_400_BAD_REQUEST)

        if not sale_document.is_confirmed_and_invoice:
            return Response({"Error": _("Only Confirmed Invoice are allowed")}, status=status.HTTP_404_NOT_FOUND)

        if sale_document.is_paid:
            return Response({"Error": _("The invoice is already paid")}, status=status.HTTP_404_NOT_FOUND)

        if not sale_document.payment_terms:
            return Response({"Error": _("Invoice does not have any payment terms")}, status=status.HTTP_404_NOT_FOUND)

        BimaErpNotificationService.send_notification_payment_sale_document_based_on_payment_term_type(
            sale_document, days_difference=3, template_code='NOTIFICATION_PAYMENT_REMINDER', message=message,
            subject=subject, send_instantly=True)
        return Response(_("NOTIFICATION_SALE_DOCUMENT_PAYMENT_LATE_SENT_SUCCESSFUL"))

    @action(detail=False, methods=['GET'], url_path="test_send_notification")
    def test_send_notification(self, request):
        BimaErpNotificationService.send_notification_for_payment_late_sale_documents()
        BimaErpNotificationService.send_notification_for_payment_reminder_sale_documents()
        return Response(_("NOTIFICATION_SALE_DOCUMENT_PAYMENT_LATE_SENT_SUCCESSFUL"))


