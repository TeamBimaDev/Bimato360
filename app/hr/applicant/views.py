from core.abstract.views import AbstractViewSet

from .filters import BimaHrApplicantFilter
from .models import BimaHrApplicant
from .serializers import BimaHrApplicantSerializer


class BimaHrApplicantViewSet(AbstractViewSet):
    queryset = BimaHrApplicant.objects.all()
    serializer_class = BimaHrApplicantSerializer
    permission_classes = []
    filterset_class = BimaHrApplicantFilter
    action_permissions = {
        'list': ['applicant.can_read'],
        'create': ['applicant.can_create'],
        'retrieve': ['applicant.can_read'],
        'update': ['applicant.can_update'],
        'partial_update': ['applicant.can_update'],
        'destroy': ['applicant.can_delete'],
        'documents': ['applicant.can_add_document'],
        'bank_accounts': ['applicant.can_add_bank_account'],
        'contacts': ['applicant.can_add_contact'],
        'addresses': ['applicant.can_add_address'],
        'delete_skill': ['applicant.can_manage_skill'],
        'add_update_skill': ['applicant.can_manage_skill']
    }
