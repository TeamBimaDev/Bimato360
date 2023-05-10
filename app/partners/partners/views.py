from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from core.abstract.views import AbstractViewSet
# Create your views here.
from partners.partners.models import BimaPartners
from rest_framework import status
from rest_framework.response import Response
from partners.partners.serializers import BimaPartnersSerializer
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactserializer

class BimaPartnersViewSet(AbstractViewSet):
    queryset = BimaPartners.objects.all()
    serializer_class = BimaPartnersSerializer
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

    def create_document(self, document_data, parent_type, parent_id):
        try:
            documents = BimaCoreDocument.objects.create(
                document_name=document_data['document_name'],
                description=document_data['description'],
                file_name=document_data['file_name'],
                file_extension=document_data['file_extension'],
                date_file=document_data['date_file'],
                file_path=document_data['file_path'],
                file_type=document_data['file_type'],
                LIST_TYPE_CHOICES=document_data['LIST_TYPE_CHOICES'],
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return documents
        except ValueError as expError:
            pass

    def create_contact(self, contact_data, parent_type, parent_id):
        try:
            contact = BimaCoreContact.objects.create(
                email=contact_data['email'],
                fax =contact_data['fax'],
                mobile =contact_data['mobile'],
                phone =contact_data['phone'],
                parent_type=parent_type,
                parent_id=parent_id,
            )
            return contact
        except ValueError as expError:
            pass
    def list_documents(self, request, public_id=None):
        model = BimaCoreDocument
        serializer = BimaCoreDocumentSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_contact(self, request, public_id=None):
        model = BimaCoreContact
        serializer = BimaCoreContactserializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def list_addresses(self, request, public_id=None):
        model = BimaCoreAddress
        serializer = BimaCoreAddressSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)

    def ajout_address_for_partners(self, request, public_id=None):
        partenaires = BimaPartners.objects.filter(public_id=public_id).first()
        partenairesContentType = ContentType.objects.filter(app_label="partners", model="Bimapartenaires").first()
        if not partenaires:
            return Response({"error": "company not found"}, status=status.HTTP_404_NOT_FOUND)


        if request.method == 'POST':
            address_data = {
                'number': request.POST.get('number'),
                'street': request.POST.get('street'),
                'street2': request.POST.get('street2'),
                'zip': request.POST.get('zip'),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'country': request.POST.get('country'),
                'parent_type': partenairesContentType,
                'parent_id':partenaires.id,

            }
            for address_data in request.data.get('address', []):
                self.create_address(address_data,partenairesContentType, partenaires.id)
            return Response({"success": "Address added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def ajout_document_for_partners(self, request, public_id=None):
        partenaires = BimaPartners.objects.filter(public_id=public_id).first()

        partenairesContentType = ContentType.objects.filter(app_label="partners", model="Bimapartenaires").first()
        if not partenaires:
            return Response({"error": "company not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            document_data = {
                'document_name': request.POST.get('document_name'),
                'description': request.POST.get('description'),
                'file_name': request.POST.get('file_name'),
                'file_extension': request.POST.get('file_extension'),
                'date_file': request.POST.get('date_file'),
                'file_path': request.POST.get('file_path'),
                'file_type': request.POST.get('file_type'),
                'LIST_TYPE_CHOICES': request.POST.get('LIST_TYPE_CHOICES'),
                'parent_type': partenairesContentType,
                'parent_id': partenaires.id,
            }
            for document_data in request.data.get('address', []):
                self.create_document(document_data, partenairesContentType, partenaires.id)
            return Response({"success": "document added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def ajout_contact_for_partners(self, request, public_id=None):
        partenaires = BimaPartners.objects.filter(public_id=public_id).first()

        partenairesContentType = ContentType.objects.filter(app_label="partners", model="Bimapartenaires").first()
        if not partenaires:
            return Response({"error": "partners not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
           contact_data = {
                ' email': request.POST.get('email'),
                'fax': request.POST.get('fax'),
                'mobile ': request.POST.get('mobile'),
                'phone': request.POST.get('phone'),
                'date_file': request.POST.get('date_file'),
                'parent_type': partenairesContentType,
                'parent_id': partenaires.id,
            }
           for contact_data in request.data.get('address', []):
               self.create_document(contact_data, partenairesContentType, partenaires.id)
           return Response({"success": "contact  added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

