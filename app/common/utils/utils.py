from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML


def render_to_pdf(template_src, context_dict={}, file_name="document.pdf"):
    template = get_template(template_src)
    html = template.render(context_dict)
    context_dict["MEDIA_URL"] = settings.MEDIA_URL
    context_dict["request_scheme"] = context_dict["request"].scheme
    context_dict["request_host"] = context_dict["request"].get_host()
    context_dict["show_price"] = context_dict.get("show_price", True)

    try:
        html_weasy = HTML(string=html)
        pdf = html_weasy.write_pdf()
    except Exception as e:

        return HttpResponse(_('An error occurred during PDF generation:<pre>') + str(e) + '</pre>')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response
