SYSTEM_PROMPT = (
    "你是一名严谨的财报分析助手。只能依据用户提供的财报原文作答，"
    "在答案中用括号标注引用页码，例如（第3页）。"
    "如果原文中没有相关信息，明确告知无法从提供的财报中找到答案，不要编造。"
)


def build_user_prompt(context: list[dict], question: str) -> str:
    parts = []
    for i, c in enumerate(context, 1):
        parts.append(f"[片段{i} | 第{c['page']}页]\n{c['text']}")
    ctx = "\n\n".join(parts)
    return (
        f"以下是财报原文片段：\n\n{ctx}\n\n"
        f"用户问题：{question}\n\n"
        f"请基于上述原文作答，并在句末用（第X页）标注依据。"
    )


def answer_question(
    store, llm, question: str, doc_id: str | None = None, top_k: int = 4
) -> dict:
    """检索 → 生成 → 返回带页码引用的答案。"""
    where = {"doc_id": doc_id} if doc_id else None
    res = store.query(question, top_k=top_k, where=where)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    context = [{"page": m["page"], "text": d} for d, m in zip(docs, metas)]
    citations = sorted({c["page"] for c in context})

    answer = llm.answer(SYSTEM_PROMPT, build_user_prompt(context, question))
    if answer is None:
        top = context[0]
        answer = (
            f"（未配置 LLM API Key，以下为最相关原文片段：）\n\n"
            f"【第{top['page']}页】{top['text']}"
        )

    return {"answer": answer, "citations": citations, "context": context}
