import logging
from tools.pdf_parser import download_pdf, extract_sections
import re


logger = logging.getLogger(__name__)


class ParsingAgent:

    def run(self, papers):

        for p in papers:

            if not p.pdf_url:
                continue

            try:

                path = download_pdf(p.pdf_url, p.id)

                sections = extract_sections(path)

                p.sections = sections

                papers["references"] = extract_references(papers["content"])

            except Exception as e:
                logger.warning(e)

        return papers
    
    def extract_references(text):

        pattern = r"\[\d+\]\s(.+)"

        refs = re.findall(pattern, text)

        return refs