import os

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.config import Config
from backend.pdf_parser import extract_pages, chunk_pages
from backend.embeddings import Embedder
from backend.vectorstore import VectorStore
from backend.llm import LLM
from backend.qa import answer_question

cfg = Config()
os.makedirs(cfg.data_dir, exist_ok=True)
os.makedirs(cfg.chroma_dir, exist_ok=True)

embedder = Embedder(cfg)
store = VectorStore(cfg.chroma_dir, embedder)
store.create_or_get("reports")
llm = LLM(cfg)

app = FastAPI(title="AI 财报分析助手 (RAG) MVP")


class AskReq(BaseModel):
    question: str
    doc_id: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "has_llm": cfg.has_llm}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    path = os.path.join(cfg.data_dir, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    pages = extract_pages(path)
    chunks = chunk_pages(pages)
    doc_id = os.path.splitext(file.filename)[0]
    store.add(chunks, doc_id)
    return {"doc_id": doc_id, "pages": len(pages), "chunks": len(chunks)}


@app.post("/ask")
def ask(req: AskReq):
    return answer_question(store, llm, req.question, doc_id=req.doc_id)
