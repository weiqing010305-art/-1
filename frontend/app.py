import requests
import streamlit as st

API = "http://localhost:8000"

st.title("AI 财报分析助手 (RAG MVP)")

uploaded = st.file_uploader("上传上市公司财报 PDF", type=["pdf"])
if uploaded:
    with st.spinner("解析并入库中..."):
        r = requests.post(f"{API}/upload", files={"file": uploaded})
        info = r.json()
    st.success(f"入库完成：{info['pages']} 页，{info['chunks']} 个文本块")

q = st.text_input("向财报提问（例如：净利润是多少？）")
if q:
    with st.spinner("生成答案..."):
        r = requests.post(f"{API}/ask", json={"question": q})
        res = r.json()
    st.markdown("### 答案")
    st.write(res.get("answer"))
    if res.get("citations"):
        st.markdown(f"**引用页码：** 第 {', '.join(str(c) for c in res['citations'])} 页")
    with st.expander("查看检索到的原文片段"):
        for c in res.get("context", []):
            st.caption(f"第 {c['page']} 页")
            st.write(c["text"])
