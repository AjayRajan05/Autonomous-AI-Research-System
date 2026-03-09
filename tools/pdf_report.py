import markdown
from weasyprint import HTML

def markdown_to_pdf(md_text, output_file):

    html_text = markdown.markdown(md_text)

    HTML(string=html_text).write_pdf(output_file)