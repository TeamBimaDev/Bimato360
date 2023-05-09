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
from hr.activity.models import BimaHrActivity
from hr.activity.serializers import BimaHrActivitySerializer

class BimaHrApplicantViewSet(AbstractViewSet):
    queryset = BimaHrApplicant.objects.all()
    serializer_class = BimaHrApplicantSerializer
    permission_classes = []
    def create_address(self, address_data, parent_type, parent_id):
        try:
            address = BimaCoreAddress.objects.create(
                number=address_data['number'],
                street=address_data['street'],
                street2=address_data['street2'],
                zip=address_data['zip'],
                city=address_data['city'],
                state_id=address_data['state'],
                country_id=address_data['country'],
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return address
        except ValueError as expError:
            pass

    def create_contact(self, contact_data, parent_type, parent_id):
        try:
            contacts = BimaCoreContact.objects.create(
                email=contact_data['email'],
                fax=contact_data['fax'],
                mobile=contact_data['mobile'],
                phone=contact_data['phone'],
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return contacts
        except ValueError as expError:
            pass

    def create_tags(self, tags_data, parent_type, parent_id):
        try:
            tags = BimaCoreTags.objects.create(
                name=tags_data['name'],
                id_manager=tags_data['id_manager'],
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return tags
        except ValueError as expError:
            pass

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        applicant = self.perform_create(serializer)
        applicantContentType = ContentType.objects.filter(app_label="hr", model="bimahrapplicant").first()
        print(applicantContentType)
        if applicantContentType:
            applicantContentType_id = applicantContentType.id
        newApplicant = BimaHrApplicant.objects.filter(public_id=serializer.data['public_id'])[0]

        if newApplicant:
            for address_data in request.data.get('address', []):
                self.create_address(address_data, applicantContentType, newApplicant.id)
            for contact_data in request.data.get('contacts', []):
                self.create_contact(contact_data, applicantContentType, newApplicant.id)
            for tags_data in request.data.get('tags', []):
                self.create_tags(tags_data, applicantContentType, newApplicant.id)
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
        serializer = BimaCoreContactserializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_tags(self, request, public_id=None):
        model = BimaCoreTags
        serializer = BimaCoreTagsserializer
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