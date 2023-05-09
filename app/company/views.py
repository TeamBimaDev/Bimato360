from core.abstract.views import AbstractViewSet
from company.models import BimaCompany
from company.serializers import BimaCompanySerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from app.core.address.models import BimaCoreAddress
from app.core.address.serializers import BimaCoreAddressSerializer


class BimaCompanyViewSet(AbstractViewSet):
    queryset = BimaCompany.objects.all()
    serializer_class = BimaCompanySerializer
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
            print(expError)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.perform_create(serializer)
        companyContentType = ContentType.objects.filter(app_label="company", model="bimacompany").first()
        if companyContentType:
                companyContentType_id = companyContentType.id
        newCompany = BimaCompany.objects.filter(public_id=serializer.data['public_id'])[0]

        if newCompany:
            for address_data in request.data.get('address', []):
                self.create_address(address_data, companyContentType, newCompany.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list_object(self, request, public_id=None, model=None, serializer=None):
        companyContentType = ContentType.objects.filter(app_label="company", model="bimacompany").first()
        if companyContentType:
            company = BimaCompany.objects.filter(public_id=public_id)[0]
            objects = model.objects.filter(parent_type_id=companyContentType.id, parent_id=company.id)
            serialized_data = serializer(objects, many=True)
            return Response(serialized_data.data)
    def list_addresses(self, request, public_id=None):
        model = BimaCoreAddress
        serializer = BimaCoreAddressSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
    def ajout_address_for_company(self, request, public_id=None):
        company = BimaCompany.objects.filter(public_id=public_id).first()
        companyContentType = ContentType.objects.filter(app_label="company", model="bimacompany").first()
        if not company:
            return Response({"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            address_data = {
                'number': request.POST.get('number'),
                'street': request.POST.get('street'),
                'street2': request.POST.get('street2'),
                'zip': request.POST.get('zip'),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'country': request.POST.get('country'),
                'parent_type': companyContentType,
                'parent_id': company.id,
            }
            for address_data in request.data.get('address', []):
                self.create_address(address_data, companyContentType, company.id)
            return Response({"success": "Address added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


