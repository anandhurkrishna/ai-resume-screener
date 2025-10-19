import io
from PyPDF2 import PdfReader
from docx import Document

async def parse_resume_bytes(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            text_pages = []
            for p in reader.pages:
                page_text = p.extract_text() or ""
                text_pages.append(page_text)
            return "\n".join(text_pages)
        elif name.endswith(".docx"):
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs]
            return "\n".join(paragraphs)
        else:
            # fallback: try decode
            return file_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        return ""  # keep simple: return empty string on parse failure