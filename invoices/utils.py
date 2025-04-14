from django.template.loader import render_to_string
import imgkit
import tempfile

def render_invoice_to_image(invoice):
    context = {'invoice': invoice}
    html_string = render_to_string('invoice_pdf.html', context)
    
    config = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as output:
        imgkit.from_string(html_string, output.name, config=config)
        image_path = output.name
    return image_path