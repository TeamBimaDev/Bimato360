

import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML


def render_to_pdf(template_src, context_dict={}, file_name="document.pdf"):
    template = get_template(template_src)
    context_dict["MEDIA_URL"] = settings.MEDIA_URL
    context_dict["request_scheme"] = context_dict["request"].scheme
    context_dict["request_host"] = context_dict["request"].get_host()
    context_dict["show_price"] = context_dict.get("show_price", True)
    html = template.render(context_dict)
    try:
        html_weasy = HTML(string=html)
        pdf = html_weasy.write_pdf()
    except Exception as e:

        return HttpResponse(_('An error occurred during PDF generation:<pre>') + str(e) + '</pre>')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response


def save_pdf_to_file(pdf_content, file_name="document.pdf"):
    pdf_dir = 'pdfs'
    if not default_storage.exists(pdf_dir):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, pdf_dir))

    pdf_path = os.path.join(pdf_dir, file_name)
    if default_storage.exists(pdf_path):
        default_storage.delete(pdf_path)

    pdf_file = ContentFile(pdf_content)
    default_storage.save(pdf_path, pdf_file)

    file_url = os.path.join(settings.MEDIA_URL, pdf_path)
    return file_url


