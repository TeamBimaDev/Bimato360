from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.translation import gettext_lazy as _

def render_to_pdf(template_src, context_dict={}, file_name="document.pdf"):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    pdf_status = pisa.CreatePDF(html, dest=response)

    if pdf_status.err:
        return HttpResponse(_('Some errors were encountered <pre>') + html + '</pre>')

    return response
