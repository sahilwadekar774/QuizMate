
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file."""
    try:
        reader = PdfReader(uploaded_file)

        if reader.is_encrypted:
            return None, "This PDF is password-protected."

        extracted_pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_pages.append(page_text)

        full_text = "\n".join(extracted_pages).strip()

        if not full_text:
            return None, (
                "No readable text was found. "
                "This may be a scanned PDF."
            )

        return full_text, None

    except Exception as error:
        return None, f"Could not read the PDF: {error}"
