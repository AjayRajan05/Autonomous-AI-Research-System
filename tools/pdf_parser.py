"""
PDF parsing utilities.

Responsible for:
- downloading PDFs
- extracting text
- detecting research paper sections
"""

import logging
import requests
from pathlib import Path
from typing import Dict
import fitz  # PyMuPDF

from tools.config_loader import load_settings


logger = logging.getLogger(__name__)

settings = load_settings()

CACHE_DIR = Path(settings["paths"]["cache_dir"])
CACHE_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# PDF DOWNLOAD
# --------------------------------------------------

def download_pdf(url: str, filename: str) -> Path:
    """
    Download PDF and store it in cache.

    Args:
        url: PDF url
        filename: name to save file as

    Returns:
        Path to downloaded file
    """

    save_path = CACHE_DIR / f"{filename}.pdf"

    if save_path.exists():
        logger.info(f"PDF already cached: {save_path}")
        return save_path

    logger.info(f"Downloading PDF: {url}")

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Saved PDF: {save_path}")

    except Exception as e:
        logger.error(f"PDF download failed: {e}")
        raise

    return save_path


# --------------------------------------------------
# TEXT EXTRACTION
# --------------------------------------------------

def extract_text(pdf_path: Path, max_pages: int = 50) -> str:
    """
    Extract raw text from PDF.

    Args:
        pdf_path: path to pdf
        max_pages: limit pages for speed

    Returns:
        full text
    """

    logger.info(f"Extracting text from: {pdf_path}")

    doc = fitz.open(pdf_path)

    text = ""

    pages_to_read = min(len(doc), max_pages)

    for page_num in range(pages_to_read):
        page = doc.load_page(page_num)
        text += page.get_text()

    doc.close()

    return text


# --------------------------------------------------
# SECTION DETECTION
# --------------------------------------------------

SECTION_KEYWORDS = {
    "abstract": ["abstract"],
    "introduction": ["introduction"],
    "methods": ["methods", "methodology"],
    "results": ["results", "experiments"],
    "conclusion": ["conclusion", "discussion"]
}


def extract_sections(pdf_path: Path) -> Dict[str, str]:
    """
    Extract common research paper sections.

    Args:
        pdf_path: path to pdf

    Returns:
        dict[str, str]
    """

    full_text = extract_text(pdf_path)

    lines = full_text.split("\n")

    sections = {k: "" for k in SECTION_KEYWORDS.keys()}

    current_section = None

    for line in lines:

        clean = line.strip().lower()

        for section, keywords in SECTION_KEYWORDS.items():
            if clean in keywords:
                current_section = section
                continue

        if current_section:
            sections[current_section] += line + " "

    return sections


# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    test_pdf = "https://arxiv.org/pdf/1706.03762.pdf"

    path = download_pdf(test_pdf, "transformer_test")

    sections = extract_sections(path)

    for name, content in sections.items():
        print("\n---", name.upper(), "---\n")
        print(content[:500])