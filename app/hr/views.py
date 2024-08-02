<<<<<<< HEAD
from common.enums.employee_enum import get_marital_status_choices, get_employment_type_choices, \
    get_work_mode_choices, get_job_type_choices, get_employee_status_choices
from common.enums.interview import get_interview_status_choices, get_interview_type_choices
from core.abstract.views import AbstractViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaHrPerson
from .serializers import BimaHrSerializer


class BimaHrViewSet(AbstractViewSet):
    queryset = BimaHrPerson.objects.all()
    serializer_class = BimaHrSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'], url_path='list_marital_status_types')
    def list_marital_status_types(self, request, *args, **kwargs):
        return Response(get_marital_status_choices())

    @action(detail=False, methods=['get'], url_path='list_employment_type_types')
    def list_employment_type_types(self, request, *args, **kwargs):
        return Response(get_employment_type_choices())

    @action(detail=False, methods=['get'], url_path='list_work_mode_types')
    def list_work_mode_types(self, request, *args, **kwargs):
        return Response(get_work_mode_choices())

    @action(detail=False, methods=['get'], url_path='list_job_type_types')
    def list_job_type_types(self, request, *args, **kwargs):
        return Response(get_job_type_choices())

    @action(detail=False, methods=['get'], url_path='list_employee_status_types')
    def list_employee_status_types(self, request, *args, **kwargs):
        return Response(get_employee_status_choices())

    @action(detail=False, methods=['get'], url_path='list_interview_status_types')
    def list_interview_status_types(self, request, *args, **kwargs):
        return Response(get_interview_status_choices())

    @action(detail=False, methods=['get'], url_path='list_interview_type_types')
    def list_interview_type_types(self, request, *args, **kwargs):
        return Response(get_interview_type_choices())
=======
from common.enums.employee_enum import get_marital_status_choices, get_employment_type_choices, \
    get_work_mode_choices, get_job_type_choices, get_employee_status_choices
from common.enums.interview import get_interview_status_choices, get_interview_type_choices
from core.abstract.views import AbstractViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaHrPerson
from .serializers import BimaHrSerializer


class BimaHrViewSet(AbstractViewSet):
    queryset = BimaHrPerson.objects.all()
    serializer_class = BimaHrSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'], url_path='list_marital_status_types')
    def list_marital_status_types(self, request, *args, **kwargs):
        return Response(get_marital_status_choices())

    @action(detail=False, methods=['get'], url_path='list_employment_type_types')
    def list_employment_type_types(self, request, *args, **kwargs):
        return Response(get_employment_type_choices())

    @action(detail=False, methods=['get'], url_path='list_work_mode_types')
    def list_work_mode_types(self, request, *args, **kwargs):
        return Response(get_work_mode_choices())

    @action(detail=False, methods=['get'], url_path='list_job_type_types')
    def list_job_type_types(self, request, *args, **kwargs):
        return Response(get_job_type_choices())

    @action(detail=False, methods=['get'], url_path='list_employee_status_types')
    def list_employee_status_types(self, request, *args, **kwargs):
        return Response(get_employee_status_choices())

    @action(detail=False, methods=['get'], url_path='list_interview_status_types')
    def list_interview_status_types(self, request, *args, **kwargs):
        return Response(get_interview_status_choices())

    @action(detail=False, methods=['get'], url_path='list_interview_type_types')
    def list_interview_type_types(self, request, *args, **kwargs):
        return Response(get_interview_type_choices())
>>>>>>> origin/ma-branch
