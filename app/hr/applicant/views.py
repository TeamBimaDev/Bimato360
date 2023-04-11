from core.abstract.views import AbstractViewSet
from .models import BimaHrApplicant
from .serializers import BimaHrApplicantSerializer
from core.address.models import BimaCoreAddress
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactserializer
from hr.interview.models import BimaHrInterview
from core.tags.models import BimaCoreTags
from hr.interview.serializers import BimaHrInterviewSerializer
from core.tags.serializers import BimaCoreTagsserializer
from hr.refuse.models import BimaHrRefuse
from hr.refuse.serializers import BimaHrRefuseSerializer

from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from hr.skill.models import BimaHrSkill
from hr.skill.serializers import BimaHrSkillSerializer

from ..activity.models import BimaHrActivity
from ..activity.serializers import BimaHrActivitySerializer


class BimaHrApplicantViewSet(AbstractViewSet):
    queryset = BimaHrApplicant.objects.all()
    serializer_class = BimaHrApplicantSerializer
    permission_classes = []
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        applicant = self.perform_create(serializer)

        for address_data in request.data.get('address', []):
            applicantContentType = ContentType.objects.filter( app_label="hr", model="bimahrapplicant").first()
            if applicantContentType:
                     applicantContentType_id = applicantContentType.id
            newApplicant = BimaHrApplicant.objects.filter(public_id=serializer.data['public_id'])[0]
            try:
                address = BimaCoreAddress.objects.create(
                    number=address_data['number'],
                    street=address_data['street'],
                    postal_code=address_data['postal_code'],
                    city=address_data['city'],
                    parent_type=ContentType.objects.filter(pk=applicantContentType_id)[0],
                    parent_id=newApplicant.id,
                )
            except ValueError as expError:
                pass
        for contact_data in  request.data.get('contacts', []):
            applicantContentType = ContentType.objects.filter( app_label="hr", model="bimahrapplicant").first()
            if applicantContentType:
                     applicantContentType_id = applicantContentType.id
            newApplicant = BimaHrApplicant.objects.filter(public_id=serializer.data['public_id'])[0]
            try:
                contacts = BimaCoreContact.objects.create(
                    email=contact_data.get('email'),
                    fax=contact_data.get('fax'),
                    mobile=contact_data.get('mobile'),
                    phone=contact_data.get('phone'),
                    parent_type=ContentType.objects.filter(pk=applicantContentType_id)[0],
                    parent_id=newApplicant.id,
                )
            except ValueError as expError:
                pass

        for tags_data in request.data.get('tags', []):
            applicantContentType = ContentType.objects.filter( app_label="hr", model="bimahrapplicant").first()
            if applicantContentType:
                     applicantContentType_id = applicantContentType.id
            newApplicant = BimaHrApplicant.objects.filter(public_id=serializer.data['public_id'])[0]
            try:
                tags = BimaCoreTags.objects.create(
                    name=tags_data.get('name'),
                    id_manager=tags_data.get('id_manager'),
                    parent_type=ContentType.objects.filter(pk=applicantContentType_id)[0],
                    parent_id=newApplicant.id,
                )
            except ValueError as expError:
                pass
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list_addresses(self, request, public_id=None):
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        if applicantContentType:
            applicant = BimaHrApplicant.objects.filter(public_id=public_id)[0]
            address = BimaCoreAddress.objects.filter(parent_type_id=applicantContentType.id, parent_id=applicant.id)
            serializer = BimaCoreAddressSerializer(address, many=True)
            return Response(serializer.data)
    def list_contacts(self, request, public_id=None):
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        if applicantContentType:
            applicant = BimaHrApplicant.objects.filter(public_id=public_id)[0]
            contacts = BimaCoreContact.objects.filter(parent_type=applicantContentType.id,parent_id=applicant.id)
            serializer = BimaCoreContactserializer(contacts, many=True)
            return Response(serializer.data)
    def list_interviews(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        interviews = BimaHrInterview.objects.filter(applicant=applicant)
        serializer = BimaHrInterviewSerializer(interviews, many=True)
        return Response(serializer.data)
    def list_tags(self, request, public_id=None):
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        if applicantContentType:
            applicant = BimaHrApplicant.objects.filter(public_id=public_id)[0]
            tags = BimaCoreTags.objects.filter(parent_type=applicantContentType.id,parent_id=applicant.id)
            serializer = BimaCoreTagsserializer(tags, many=True)
            return Response(serializer.data)
    def list_refuse(self, request, public_id=None):
        applicant = BimaHrApplicant.objects.get(public_id=public_id)
        refuse = BimaHrRefuse.objects.filter(applicant=applicant)
        serializer = BimaHrRefuseSerializer(refuse, many=True)
        return Response(serializer.data)

    def list_documents(self, request, public_id=None):
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        if applicantContentType:
            applicant = BimaHrApplicant.objects.filter(public_id=public_id)[0]
            document = BimaCoreDocument.objects.filter(parent_type=applicantContentType.id,parent_id=applicant.id)
            serializer = BimaCoreDocumentSerializer(document, many=True)
            return Response(serializer.data)
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