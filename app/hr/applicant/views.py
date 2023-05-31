from core.abstract.views import AbstractViewSet
from .models import BimaHrApplicant
from .serializers import BimaHrApplicantSerializer
from core.address.models import BimaCoreAddress
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer
from hr.interview.models import BimaHrInterview
from hr.interview.serializers import BimaHrInterviewSerializer
from hr.refuse.models import BimaHrRefuse
from hr.refuse.serializers import BimaHrRefuseSerializer
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from hr.skill.models import BimaHrSkill
from hr.skill.serializers import BimaHrSkillSerializer
from hr.activity.models import BimaHrActivity
from hr.activity.serializers import BimaHrActivitySerializer

class BimaHrApplicantViewSet(AbstractViewSet):
    queryset = BimaHrApplicant.objects.all()
    serializer_class = BimaHrApplicantSerializer
    permission_classes = []


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        applicant = self.perform_create(serializer)
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        newApplicant = BimaHrApplicant.objects.filter(public_id=serializer.data['public_id'])[0]
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list_object(self, request, public_id=None, model=None, serializer=None):
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        if applicantContentType:
            applicant = BimaHrApplicant.objects.filter(public_id=public_id)[0]
            objects = model.objects.filter(parent_type_id=applicantContentType.id, parent_id=applicant.id)
            serialized_data = serializer(objects, many=True)
            return Response(serialized_data.data)
    def list_addresses(self, request, public_id=None):
        model = BimaCoreAddress
        serializer = BimaCoreAddressSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_contacts(self, request, public_id=None):
        model = BimaCoreContact
        serializer = BimaCoreContactSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_documents(self, request, public_id=None):
        model = BimaCoreDocument
        serializer = BimaCoreDocumentSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_skills(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        skills = BimaHrSkill.objects.filter(applicant=applicant)
        serializer = BimaHrSkillSerializer(skills, many=True)
        return Response(serializer.data)
    def list_activities(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        activities = BimaHrActivity.objects.filter(applicant=applicant)
        serializer = BimaHrActivitySerializer(activities, many=True)
        return Response(serializer.data)
    def list_refuse(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        refuse = BimaHrRefuse.objects.filter(applicant=applicant)
        serializer = BimaHrRefuseSerializer(refuse, many=True)
        return Response(serializer.data)
    def list_interviews(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        interviews = BimaHrInterview.objects.filter(applicant=applicant)
        serializer = BimaHrInterviewSerializer(interviews, many=True)
        return Response(serializer.data)