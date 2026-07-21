import fitz


def extract_pages(pdf_path: str) -> list[dict]:
    """用 PyMuPDF 抽取每一页文本，保留页码（从 1 开始）。"""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({"page": i + 1, "text": text})
    doc.close()
    return pages


def chunk_pages(
    pages: list[dict], chunk_size: int = 800, chunk_overlap: int = 100
) -> list[dict]:
    """按字符切块并保留来源页码。块大小为 chunk_size，重叠 chunk_overlap。"""
    chunks = []
    step = max(1, chunk_size - chunk_overlap)
    for p in pages:
        text = p["text"]
        if not text.strip():
            continue
        for start in range(0, len(text), step):
            piece = text[start : start + chunk_size].strip()
            if piece:
                chunks.append({"page": p["page"], "text": piece})
    return chunks
