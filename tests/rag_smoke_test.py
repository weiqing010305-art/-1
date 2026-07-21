"""无 API Key 也能跑的连通性测试：生成示例财报 PDF，验证整条 RAG 管线。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fitz

from backend.config import Config
from backend.pdf_parser import extract_pages, chunk_pages
from backend.embeddings import Embedder
from backend.vectorstore import VectorStore
from backend.llm import LLM
from backend.qa import answer_question

cfg = Config()
os.makedirs(cfg.data_dir, exist_ok=True)
os.makedirs(cfg.chroma_dir, exist_ok=True)

pages_text = [
    "XX 股份有限公司 2023 年年度报告。本公司主要从事智能制造业务。",
    "利润表摘要：本年度营业收入 58.2 亿元，净利润为 12.3 亿元，同比增长 8.5%。",
    "现金流量表：经营活动产生的现金流量净额为 5.6 亿元，投资活动流出 3.2 亿元。",
    "风险因素：本公司面临的主要风险包括原材料价格波动、汇率变动以及行业竞争加剧。",
]

# PyMuPDF 内置 CJK 字体（china-s = 简体中文），用于生成可正确抽取的测试 PDF。
pdf_path = os.path.join(cfg.data_dir, "sample_report.pdf")
doc = fitz.open()
for t in pages_text:
    page = doc.new_page()
    page.insert_text(fitz.Point(50, 800), t, fontname="china-s", fontsize=12)
doc.save(pdf_path)
doc.close()
print("sample pdf created:", pdf_path)

embedder = Embedder(cfg)
store = VectorStore(cfg.chroma_dir, embedder)
try:
    store.client.delete_collection("reports")
except Exception:
    pass
store.create_or_get("reports")
llm = LLM(cfg)

pages = extract_pages(pdf_path)
chunks = chunk_pages(pages)
store.add(chunks, "sample_report")
print(f"ingested pages={len(pages)} chunks={len(chunks)}")

for q, expected_page in [("净利润是多少？", 2), ("经营活动现金流情况如何？", 3), ("公司面临哪些风险？", 4)]:
    res = answer_question(store, llm, q, doc_id="sample_report")
    print("\nQ:", q)
    print("A:", res["answer"])
    print("citations:", res["citations"])
    top_page = res["context"][0]["page"]
    status = "PASS" if top_page == expected_page else "FAIL"
    print(f"[{status}] top-1 page={top_page} (expected={expected_page})")
