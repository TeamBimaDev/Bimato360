<<<<<<< HEAD
from common.enums.file_type import FileTypeCompany
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.contrib.contenttypes.models import ContentType

from .fake_sale import generate_fake_data
from .models import BimaCompany
from .serializers import BimaCompanySerializer


def fetch_company_data(company):
    company_serializer = BimaCompanySerializer(company)
    logo = get_favorite_logo(company)
    logo_data = BimaCoreDocumentSerializer(logo).data if logo else None

    response_data = {
        'company': company_serializer.data,
        'favorite_logo': logo_data,
        'default_sale_document_pdf_format': company_serializer.data.get('default_pdf_invoice_format',
                                                                        return_default_sale_document_pdf_file())
    }

    return response_data


def get_favorite_logo(company):
    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(company),
        parent_id=company.id,
        file_type=FileTypeCompany.COMPANY_LOGO.name,
        is_favorite=True
    ).first()


def return_default_sale_document_pdf_file():
    return "sale_document_elegant.html"


def get_context(request, request_data):
    company = BimaCompany.objects.first()
    company.default_font_family = request_data.get('font_family')
    company.default_color = request_data.get('default_color')
    company.show_template_header = request_data.get('show_template_header')
    company.show_template_footer = request_data.get('show_template_footer')
    company.show_template_logo = request_data.get('show_template_logo')
    context = generate_fake_data()
    context['document_title'] = context['sale_document'].type
    context['request'] = request
    context['company_data'] = fetch_company_data(company)
    return context
=======
from common.enums.file_type import FileTypeCompany
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from django.contrib.contenttypes.models import ContentType

from .fake_sale import generate_fake_data
from .models import BimaCompany
from .serializers import BimaCompanySerializer


def fetch_company_data(company):
    company_serializer = BimaCompanySerializer(company)
    logo = get_favorite_logo(company)
    logo_data = BimaCoreDocumentSerializer(logo).data if logo else None

    response_data = {
        'company': company_serializer.data,
        'favorite_logo': logo_data,
        'default_sale_document_pdf_format': company_serializer.data.get('default_pdf_invoice_format',
                                                                        return_default_sale_document_pdf_file())
    }

    return response_data


def get_favorite_logo(company):
    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(company),
        parent_id=company.id,
        file_type=FileTypeCompany.COMPANY_LOGO.name,
        is_favorite=True
    ).first()


def return_default_sale_document_pdf_file():
    return "sale_document_elegant.html"


def get_context(request, request_data):
    company = BimaCompany.objects.first()
    company.default_font_family = request_data.get('font_family')
    company.default_color = request_data.get('default_color')
    company.show_template_header = request_data.get('show_template_header')
    company.show_template_footer = request_data.get('show_template_footer')
    company.show_template_logo = request_data.get('show_template_logo')
    context = generate_fake_data()
    context['document_title'] = context['sale_document'].type
    context['request'] = request
    context['company_data'] = fetch_company_data(company)
    return context
>>>>>>> origin/ma-branch
