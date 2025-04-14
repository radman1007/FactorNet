from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

def render_invoice_to_pdf(invoice):
    context = {'invoice': invoice}
    html_string = render_to_string('invoice_pdf.html', context)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
        HTML(string=html_string).write_pdf(target=output.name)
        pdf_file_path = output.name
    return pdf_file_path