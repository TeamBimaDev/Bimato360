from common.enums.file_type import FileTypeCompany
from django.contrib.contenttypes.models import ContentType
from .serializers import BimaCompanySerializer
from core.document.serializers import BimaCoreDocumentSerializer
from core.document.models import BimaCoreDocument


def fetch_company_data(company):
    company_serializer = BimaCompanySerializer(company)
    logo = get_favorite_logo(company)
    logo_data = BimaCoreDocumentSerializer(logo).data if logo else None

    response_data = {
        'company': company_serializer.data,
        'favorite_logo': logo_data
    }

    return response_data


def get_favorite_logo(company):
    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(company),
        parent_id=company.id,
        file_type=FileTypeCompany.COMPANY_LOGO.name,
        is_favorite=True
    ).first()