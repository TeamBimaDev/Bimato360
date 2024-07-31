<<<<<<< HEAD
from common.enums.activity_status import PresenceStatus
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.pagination import DefaultPagination
from core.abstract.views import AbstractViewSet
from core.document.models import get_documents_for_parent_entity, BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from hr.employee.models import BimaHrEmployee
from hr.models import BimaHrPerson
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import BimaHrActivityFilter
from .models import BimaHrActivity, BimaHrActivityParticipant
from .serializers import BimaHrActivitySerializer, BimaHrActivityParticipantSerializer, BimaHrActivityHistorySerializer
from .service import BimaHrActivityNotificationService, BimaHrActivityService


class BimaHrActivityViewSet(AbstractViewSet):
    queryset = BimaHrActivity.objects.all()
    serializer_class = BimaHrActivitySerializer
    ordering = ["-start_date"]
    filterset_class = BimaHrActivityFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['activity.can_read'],
        'create': ['activity.can_create'],
        'retrieve': ['activity.can_read'],
        'update': ['activity.can_update'],
        'partial_update': ['activity.can_update'],
        'destroy': ['activity.can_delete'],
        'get_participants': ['activity.can_manage_participants'],
        'add_participant': ['activity.can_manage_participants'],
        'remove_participant': ['activity.can_manage_participants'],
    }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            activity = BimaHrActivity.objects.get(public_id=response.data['id'])
            BimaHrActivityNotificationService.send_bulk_invitation_notifications(activity)
        return response

    @action(detail=True, methods=['POST'], url_path="send_reminder")
    def send_reminder(self, request, pk=None):
        activity = self.get_object()
        if activity.start_date > timezone.now():
            return Response({'detail': 'Cannot send reminder notifications for future activities.'},
                            status=status.HTTP_400_BAD_REQUEST)
        BimaHrActivityNotificationService.send_bulk_invitation_notifications(activity)
        return Response({'detail': 'Reminder notifications sent successfully.'})

    @action(detail=True, methods=['GET'], url_path="get_participants")
    def get_participants(self, request, pk=None):
        activity = self.get_object()
        participants = BimaHrActivityParticipant.objects.filter(activity=activity)
        serializer = BimaHrActivityParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path="add_participant")
    def add_participant(self, request, pk=None):
        activity = self.get_object()
        person_public_id = request.data.get('person_public_id')
        participant_exists = BimaHrActivityParticipant.objects.filter(activity=activity,
                                                                      person__public_id=person_public_id).exists()

        if participant_exists:
            return Response({'error': 'This person is already a participant in the activity.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = BimaHrActivityParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(activity=activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], url_path="remove_participant")
    def remove_participant(self, request, pk=None):
        activity = self.get_object()
        participant_id = request.data.get('participant_id')
        try:
            participant = BimaHrActivityParticipant.objects.get(activity=activity, public_id=participant_id)
            participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BimaHrActivityParticipant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], url_path="change_participant_status")
    def change_participant_status(self, request, pk=None):
        activity = self.get_object()

        if activity.end_date < timezone.now():
            return Response({'error': 'Cannot change status for a past activity.'}, status=status.HTTP_400_BAD_REQUEST)

        person_public_id = request.data.get('person_public_id')
        new_status = request.data.get('status')

        if new_status not in [st.name for st in PresenceStatus]:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        person = get_object_or_404(BimaHrPerson, public_id=person_public_id)
        employee = get_object_or_404(BimaHrEmployee, public_id=person_public_id)

        if request.user != employee.user:
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        participant = get_object_or_404(BimaHrActivityParticipant, activity=activity, person=person)

        participant.presence_status = new_status
        participant.save()

        return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="my_activities")
    def my_activities(self, request):
        user = request.user

        try:
            employee = BimaHrEmployee.objects.get(user=user)
        except BimaHrEmployee.DoesNotExist:
            return Response({'error': 'The connected user is not linked to any employee.'},
                            status=status.HTTP_400_BAD_REQUEST)

        activities = BimaHrActivityParticipant.objects.filter(person=employee)

        filtered_activities = self.filterset_class(self.request.GET, queryset=activities).qs

        paginator = DefaultPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_activities, request)

        serializer = BimaHrActivityParticipantSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def get_object(self):
        obj = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def list_documents(self, request, *args, **kwargs):
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(activity)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(activity, document_data)
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
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=activity.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    @action(detail=True, methods=["GET"], url_path="get_activity_history")
    def get_activity_history(self, request, pk=None):
        activity = self.get_object()
        history = activity.history.all()
        if not history.exists():
            return Response([], status=status.HTTP_200_OK)

        serialized_history = BimaHrActivityHistorySerializer(history, many=True).data
        grouped_history = BimaHrActivityService.group_by_date(
            serialized_history
        )
        response_data = [
            {"date": key, "changes": value} for key, value in grouped_history.items()
        ]
        return Response(response_data)
=======
from datetime import datetime

from common.enums.activity_status import PresenceStatus
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.document.models import get_documents_for_parent_entity, BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from hr.employee.models import BimaHrEmployee
from hr.models import BimaHrPerson
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaHrActivity, BimaHrActivityParticipant
from .serializers import BimaHrActivitySerializer, BimaHrActivityParticipantSerializer, BimaHrActivityHistorySerializer
from .service import BimaHrActivityNotificationService, BimaHrActivityService


class BimaHrActivityViewSet(AbstractViewSet):
    queryset = BimaHrActivity.objects.all()
    serializer_class = BimaHrActivitySerializer
    ordering = ["-start_date"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['activity.can_read'],
        'create': ['activity.can_create'],
        'retrieve': ['activity.can_read'],
        'update': ['activity.can_update'],
        'partial_update': ['activity.can_update'],
        'destroy': ['activity.can_delete'],
        'get_participants': ['activity.can_manage_participants'],
        'add_participant': ['activity.can_manage_participants'],
        'remove_participant': ['activity.can_manage_participants'],
    }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            activity = BimaHrActivity.objects.get(public_id=response.data['id'])
            BimaHrActivityNotificationService.send_bulk_invitation_notifications(activity)
        return response

    @action(detail=True, methods=['POST'], url_path="send_reminder")
    def send_reminder(self, request, pk=None):
        activity = self.get_object()
        if activity.start_date > timezone.now():
            return Response({'detail': 'Cannot send reminder notifications for future activities.'},
                            status=status.HTTP_400_BAD_REQUEST)
        BimaHrActivityNotificationService.send_bulk_invitation_notifications(activity)
        return Response({'detail': 'Reminder notifications sent successfully.'})

    @action(detail=True, methods=['GET'], url_path="get_participants")
    def get_participants(self, request, pk=None):
        activity = self.get_object()
        participants = BimaHrActivityParticipant.objects.filter(activity=activity)
        serializer = BimaHrActivityParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path="add_participant")
    def add_participant(self, request, pk=None):
        activity = self.get_object()
        person_public_id = request.data.get('person_public_id')
        participant_exists = BimaHrActivityParticipant.objects.filter(activity=activity,
                                                                      person__public_id=person_public_id).exists()

        if participant_exists:
            return Response({'error': 'This person is already a participant in the activity.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = BimaHrActivityParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(activity=activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], url_path="remove_participant")
    def remove_participant(self, request, pk=None):
        activity = self.get_object()
        participant_id = request.data.get('participant_id')
        try:
            participant = BimaHrActivityParticipant.objects.get(activity=activity, public_id=participant_id)
            participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BimaHrActivityParticipant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], url_path="change_participant_status")
    def change_participant_status(self, request, pk=None):
        activity = self.get_object()

        if activity.end_date < datetime.now():
            return Response({'error': 'Cannot change status for a past activity.'}, status=status.HTTP_400_BAD_REQUEST)

        person_public_id = request.data.get('person_public_id')
        new_status = request.data.get('status')

        if new_status not in PresenceStatus._member_names_:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        person = get_object_or_404(BimaHrPerson, public_id=person_public_id)

        if not hasattr(person, 'employee') or request.user != person.employee.user:
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        participant = get_object_or_404(BimaHrActivityParticipant, activity=activity, person=person)

        participant.presence_status = new_status
        participant.save()

        return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="my_activities")
    def my_activities(self, request):
        user = request.user

        try:
            employee = BimaHrEmployee.objects.get(user=user)
        except BimaHrEmployee.DoesNotExist:
            return Response({'error': 'The connected user is not linked to any employee.'},
                            status=status.HTTP_400_BAD_REQUEST)

        activities = BimaHrActivityParticipant.objects.filter(person=employee)

        serializer = BimaHrActivityParticipantSerializer(activities, many=True)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def list_documents(self, request, *args, **kwargs):
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(activity)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(activity, document_data)
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
        activity = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=activity.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    @action(detail=True, methods=["GET"], url_path="get_activity_history")
    def get_activity_history(self, request, pk=None):
        activity = self.get_object()
        history = activity.history.all()
        if not history.exists():
            return Response([], status=status.HTTP_200_OK)

        serialized_history = BimaHrActivityHistorySerializer(history, many=True).data
        grouped_history = BimaHrActivityService.group_by_date(
            serialized_history
        )
        response_data = [
            {"date": key, "changes": value} for key, value in grouped_history.items()
        ]
        return Response(response_data)
>>>>>>> origin/ma-branch
