# AI 财报分析助手（RAG）— 主线 1

> 金融科技作品集 · 三条递进主线第一条 | MVP 已跑通 ✅

上传上市公司财报 PDF，自动抽取文本、向量化入库，支持**自然语言提问 + 带页码引用**的答案。技术栈集中、做深一件事。

## 演示

```
用户：净利润是多少？
系统：【第2页】利润表摘要：本年度营业收入 58.2 亿元，净利润为 12.3 亿元，同比增长 8.5%。
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Streamlit |
| 后端 | FastAPI |
| PDF 解析 | PyMuPDF (fitz) |
| 向量库 | Chroma (PersistentClient) |
| Embedding | OpenAI text-embedding-3-small / 本地哈希兜底 |
| LLM | OpenAI 兼容接口（DeepSeek/通义/vLLM 均可） |

## 项目结构

```
project1/
├── backend/
│   ├── config.py         # .env 配置读取
│   ├── pdf_parser.py     # PDF 逐页抽取 + 切块（保留页码）
│   ├── embeddings.py     # Embedding：远程 API + 本地哈希离线兜底
│   ├── vectorstore.py    # Chroma 向量库封装
│   ├── llm.py            # OpenAI 兼容 LLM 客户端
│   ├── qa.py             # RAG 编排：检索 → LLM 生成 → 带页码引用
│   └── main.py           # FastAPI 入口（/health /upload /ask）
├── frontend/
│   └── app.py            # Streamlit 交互界面
├── tests/
│   └── rag_smoke_test.py # 冒烟测试：无 Key 跑通全管线（3/3 PASS）
├── docs/
│   └── PRD.md            # 产品需求文档
├── .env.example          # 环境变量模板
├── requirements.txt      # Python 依赖
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt

# 2. 配置 LLM（可选）
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY 等

# 3. 启动后端
uvicorn backend.main:app --reload --port 8000

# 4. 启动前端（另开终端）
streamlit run frontend/app.py
```

## 无 API Key 也能跑

未配置 `OPENAI_API_KEY` 时，embedding 使用本地哈希兜底，问答返回 **Top-1 最相关原文片段 + 页码**，保证整条管线可离线验证。配好 Key 后自动切真实 LLM。

## 冒烟测试

```bash
python tests/rag_smoke_test.py
```

生成 4 页示例财报 PDF，验证全流程：抽取 → 切块 → 入库 → 检索 → 排名 → 回答。

```
净利润是多少？            → [PASS] top-1 page=2
经营活动现金流情况如何？   → [PASS] top-1 page=3
公司面临哪些风险？        → [PASS] top-1 page=4
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/upload` | 上传 PDF，返回 `{doc_id, pages, chunks}` |
| POST | `/ask` | 提问，返回 `{answer, citations, context}` |

## 路线图

```
✅ MVP（当前）  →  🔜 V1.1 做深财报  →  🔜 主线 2 股票分析  →  🔜 主线 3 多 Agent
   已跑通             自动抽取+对比           +行情+回测            一句话分析
```

详见 [`docs/PRD.md`](docs/PRD.md)。

## 三条主线

| 主线 | 内容 | 技术增量 |
|------|------|----------|
| **1. AI 财报分析助手** ← 当前 | RAG + 财报深度问答 | FastAPI + Chroma + LLM |
| 2. 股票分析平台 | 在本项目上加行情/指标/回测/看板 | akshare + TA-Lib + 回测引擎 |
| 3. 股票研究 Agent | 多 Agent 编排，一句话出研报 | LangChain/LangGraph + 工具调用 |

三条主线递进、代码复用，后者在前者基础上构建。
