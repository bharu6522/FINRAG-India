# app.py
import os
import json
import time
import streamlit as st
from openai import OpenAI
import numpy as np
import faiss

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="FinRAG — Financial Document Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

/* Header */
.fin-header {
    background: linear-gradient(135deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
    border: 1px solid #00C49A33;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.fin-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #00C49A15 0%, transparent 70%);
    pointer-events: none;
}
.fin-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #E6EDF3;
    margin: 0;
    letter-spacing: -1px;
}
.fin-title span { color: #00C49A; }
.fin-subtitle {
    color: #8B949E;
    font-size: 0.85rem;
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
}

/* Source cards */
.source-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-left: 3px solid #00C49A;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.78rem;
    color: #8B949E;
    transition: border-color 0.2s;
}
.source-card:hover { border-left-color: #58C4A4; }
.source-score {
    display: inline-block;
    background: #00C49A22;
    color: #00C49A;
    padding: 1px 8px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-left: 8px;
}

/* Answer box */
.answer-box {
    background: #161B22;
    border: 1px solid #00C49A44;
    border-radius: 10px;
    padding: 1.5rem;
    line-height: 1.8;
    color: #E6EDF3;
    font-size: 0.9rem;
}

/* Stat chips */
.stat-chip {
    display: inline-block;
    background: #21262D;
    border: 1px solid #30363D;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: #8B949E;
    margin: 3px;
}
.stat-chip b { color: #00C49A; }

/* Chat message styling */
.chat-user {
    background: #1C2128;
    border-radius: 12px 12px 4px 12px;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0;
    border: 1px solid #30363D;
    color: #E6EDF3;
    font-size: 0.88rem;
}
.chat-bot {
    background: #161B22;
    border-radius: 12px 12px 12px 4px;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0;
    border: 1px solid #00C49A33;
    color: #E6EDF3;
    font-size: 0.88rem;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }

/* Input styling */
.stTextInput > div > div > input {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #E6EDF3 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00C49A !important;
    box-shadow: 0 0 0 2px #00C49A22 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────
STORE_DIR   = "vector_store"
EMBED_MODEL = "text-embedding-3-small"
GPT_MODEL   = "gpt-4o-mini"

@st.cache_resource(show_spinner=False)
def load_vector_store():
    """Load FAISS index + metadata once and cache."""
    index = faiss.read_index(f"{STORE_DIR}/index.faiss")
    with open(f"{STORE_DIR}/metadata.json") as f:
        metadata = json.load(f)
    return index, metadata

def get_client():
    api_key = st.session_state.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
    return OpenAI(api_key=api_key)

def embed_query(query: str) -> np.ndarray:
    client = get_client()
    resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
    vec = np.array(resp.data[0].embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(vec)
    return vec

def retrieve(query: str, index, metadata, top_k: int = 5):
    vec = embed_query(query)
    scores, indices = index.search(vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            chunk = metadata[idx].copy()
            chunk["score"] = round(float(score), 4)
            results.append(chunk)
    return results

def generate_answer(query: str, chunks: list[dict]) -> str:
    client = get_client()
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']} | Page {c['page']}]\n{c['text']}"
        for c in chunks
    )
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": (
                "You are a financial analyst assistant for Indian regulatory documents "
                "(RBI, SEBI) and corporate reports. Answer ONLY from the provided context. "
                "Cite source and page for each claim. Use ₹ for INR amounts."
            )},
            {"role": "user", "content": (
                f"Context:\n{context}\n\nQuestion: {query}\n\n"
                "Answer concisely with citations."
            )}
        ],
        max_tokens=800,
        temperature=0.2,
        stream=True
    )
    return response  # streamed

# ── Session state ──────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "top_k" not in st.session_state:
    st.session_state.top_k = 5
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-..."
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.markdown("---")
    st.markdown("### 🎛️ Retrieval Settings")

    st.session_state.top_k = st.slider(
        "Chunks to retrieve (top-k)", 
        min_value=1, max_value=10, value=5
    )

    model_choice = st.selectbox(
        "GPT Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )
    GPT_MODEL = model_choice

    st.markdown("---")
    st.markdown("### 📂 Knowledge Base")

    store_exists = os.path.exists(f"{STORE_DIR}/index.faiss")
    if store_exists:
        with open(f"{STORE_DIR}/metadata.json") as f:
            meta = json.load(f)
        sources = list(set(m["source"] for m in meta))
        st.success(f"✅ {len(meta)} chunks loaded")
        st.markdown(f"**{len(sources)} documents indexed:**")
        for s in sources:
            count = sum(1 for m in meta if m["source"] == s)
            st.markdown(f"<div class='stat-chip'>📄 {s[:25]}... <b>({count})</b></div>",
                        unsafe_allow_html=True)
    else:
        st.warning("⚠️ No vector store found.\nRun `main.py` first.")

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    st.markdown(f"<div class='stat-chip'>Queries: <b>{st.session_state.total_queries}</b></div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='stat-chip'>Top-k: <b>{st.session_state.top_k}</b></div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='stat-chip'>Model: <b>{GPT_MODEL}</b></div>",
                unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Main Panel ─────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="fin-header">
    <div class="fin-title">Fin<span>RAG</span></div>
    <div class="fin-subtitle">
        FINANCIAL DOCUMENT INTELLIGENCE · RBI · SEBI · ANNUAL REPORTS · 2024–25
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_chat, tab_docs, tab_about = st.tabs(["💬 Chat", "📄 Documents", "ℹ️ About"])

# ── TAB 1: Chat ────────────────────────────────────────────────────────────
with tab_chat:
    if not store_exists:
        st.error("Vector store not found. Run the pipeline first:\n```\npython main.py\n```")
        st.stop()

    if not st.session_state.api_key and not os.environ.get("OPENAI_API_KEY"):
        st.warning("🔑 Add your OpenAI API key in the sidebar to start.")
        st.stop()

    # Load store
    index, metadata = load_vector_store()

    # Suggested questions
    if not st.session_state.messages:
        st.markdown("#### 💡 Try asking:")
        cols = st.columns(2)
        suggestions = [
            "What are RBI's digital lending guidelines?",
            "Summarize Bajaj Finserv's FY25 revenue",
            "What are SEBI's margin trading rules?",
            "What is the NPA ratio mentioned in the report?",
        ]
        for i, s in enumerate(suggestions):
            if cols[i % 2].button(s, use_container_width=True, key=f"sug_{i}"):
                st.session_state.messages.append({"role": "user", "content": s})
                st.rerun()

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>',
                            unsafe_allow_html=True)
                if "sources" in msg:
                    with st.expander(f"📎 {len(msg['sources'])} sources retrieved"):
                        for s in msg["sources"]:
                            st.markdown(
                                f'<div class="source-card">'
                                f'📄 <b>{s["source"]}</b> · Page {s["page"]}'
                                f'<span class="source-score">{s["score"]:.3f}</span>'
                                f'<br><small>{s["text"][:150]}...</small>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

    # Input
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        user_input = col1.text_input(
            "Ask about your financial documents...",
            placeholder="e.g. What are the key risk factors in the annual report?",
            label_visibility="collapsed"
        )
        submitted = col2.form_submit_button("Send →", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.total_queries += 1

        with st.spinner("🔍 Searching documents..."):
            chunks = retrieve(user_input, index, metadata, st.session_state.top_k)

        # Stream answer
        answer_placeholder = st.empty()
        full_answer = ""

        with st.spinner(""):
            stream = generate_answer(user_input, chunks)
            for chunk_delta in stream:
                delta = chunk_delta.choices[0].delta.content or ""
                full_answer += delta
                answer_placeholder.markdown(
                    f'<div class="answer-box">{full_answer}▌</div>',
                    unsafe_allow_html=True
                )

        answer_placeholder.empty()
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_answer,
            "sources": chunks
        })
        st.rerun()


# ── TAB 2: Documents ───────────────────────────────────────────────────────
with tab_docs:
    st.markdown("### 📄 Indexed Documents")
    if store_exists:
        with open(f"{STORE_DIR}/metadata.json") as f:
            all_meta = json.load(f)

        sources = list(set(m["source"] for m in all_meta))
        selected = st.selectbox("Select document", sources)

        doc_chunks = [m for m in all_meta if m["source"] == selected]
        pages = sorted(set(m["page"] for m in doc_chunks))

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Chunks", len(doc_chunks))
        col2.metric("Pages Indexed", len(pages))
        col3.metric("Avg Chunk Size",
                    f"{int(np.mean([m['char_count'] for m in doc_chunks]))} chars")

        st.markdown("---")
        st.markdown("#### 🔍 Browse Chunks")
        page_filter = st.selectbox("Page", ["All"] + [str(p) for p in pages])

        filtered = (doc_chunks if page_filter == "All"
                    else [m for m in doc_chunks if str(m["page"]) == page_filter])

        for i, chunk in enumerate(filtered[:20]):  # show max 20
            with st.expander(f"Chunk {i+1} · Page {chunk['page']} · {chunk['char_count']} chars"):
                st.code(chunk["text"], language=None)
    else:
        st.info("Run the pipeline first to index documents.")


# ── TAB 3: About ───────────────────────────────────────────────────────────
# ── TAB 3: About ───────────────────────────────────────────────────────────
with tab_about:

    # ── Pipeline Architecture ──────────────────────────────────────────────
    st.markdown("### 🏗️ Pipeline Architecture")
    st.markdown("""
    <div style="background:#161B22; border:1px solid #30363D; border-radius:10px; padding:1.2rem; font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#8B949E; line-height:2;">
    📂 <b style="color:#E6EDF3">PDFs</b> (RBI / SEBI / Annual Reports)
    &nbsp;&nbsp;&nbsp;↓
    🔍 <b style="color:#00C49A">PyPDF2</b> — Extract raw text page by page
    &nbsp;&nbsp;&nbsp;↓
    🧹 <b style="color:#00C49A">clean_text()</b> — Strip headers, page numbers, artifacts
    &nbsp;&nbsp;&nbsp;↓
    ✂️  <b style="color:#00C49A">RecursiveCharacterTextSplitter</b> — chunk=500, overlap=50
    &nbsp;&nbsp;&nbsp;↓
    🔢 <b style="color:#00C49A">OpenAI text-embedding-3-small</b> — 1536-dim vectors
    &nbsp;&nbsp;&nbsp;↓
    🗄️  <b style="color:#00C49A">FAISS IndexFlatIP</b> — Cosine similarity search
    &nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↑ user query embedded
    🎯 <b style="color:#E6EDF3">Top-K Chunks</b> retrieved by similarity score
    &nbsp;&nbsp;&nbsp;↓
    🤖 <b style="color:#00C49A">GPT-4o-mini</b> — Answer with citations
    &nbsp;&nbsp;&nbsp;↓
    💬 <b style="color:#E6EDF3">Cited Answer</b> shown in Chat tab
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tech Stack Table ───────────────────────────────────────────────────
    st.markdown("### ⚙️ Technical Stack")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        | Component | Technology |
        |-----------|-----------|
        | PDF Parsing | PyPDF2 |
        | Text Cleaning | Regex + custom rules |
        | Chunking | LangChain RecursiveCharacterTextSplitter |
        | Embeddings | text-embedding-3-small (1536d) |
        """)

    with col2:
        st.markdown("""
        | Component | Technology |
        |-----------|-----------|
        | Vector Store | FAISS IndexFlatIP |
        | Similarity | Cosine (L2-normalized) |
        | Generation | GPT-4o-mini (streaming) |
        | UI | Streamlit |
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chunk Settings Visual ──────────────────────────────────────────────
    st.markdown("### ✂️ Chunking Strategy")

    st.markdown("""
    <div style="background:#161B22; border:1px solid #30363D; border-radius:10px; padding:1.2rem;">
        <div style="font-size:0.78rem; color:#8B949E; margin-bottom:0.8rem;">
            How a 1200-char paragraph is split into overlapping chunks:
        </div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <div style="background:#00C49A22; border:1px solid #00C49A; border-radius:6px; padding:6px 12px; font-size:0.75rem; color:#00C49A;">
                Chunk 1<br><span style="color:#8B949E;">chars 0–500</span>
            </div>
            <div style="background:#21262D; border:1px dashed #30363D; border-radius:6px; padding:6px 12px; font-size:0.75rem; color:#8B949E;">
                ← 50 overlap →
            </div>
            <div style="background:#00C49A22; border:1px solid #00C49A; border-radius:6px; padding:6px 12px; font-size:0.75rem; color:#00C49A;">
                Chunk 2<br><span style="color:#8B949E;">chars 450–950</span>
            </div>
            <div style="background:#21262D; border:1px dashed #30363D; border-radius:6px; padding:6px 12px; font-size:0.75rem; color:#8B949E;">
                ← 50 overlap →
            </div>
            <div style="background:#00C49A22; border:1px solid #00C49A; border-radius:6px; padding:6px 12px; font-size:0.75rem; color:#00C49A;">
                Chunk 3<br><span style="color:#8B949E;">chars 900–1200</span>
            </div>
        </div>
        <div style="margin-top:1rem; font-size:0.75rem; color:#8B949E;">
            <b style="color:#E6EDF3;">Separator priority:</b>
            &nbsp; ¶ Paragraph → ↵ Newline → . Sentence → Space → Character
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live Cost Calculator ───────────────────────────────────────────────
    st.markdown("### 💰 Cost Estimator")

    col1, col2, col3 = st.columns(3)
    num_pdfs    = col1.number_input("Number of PDFs",      min_value=1,  max_value=50,   value=8)
    pages_each  = col2.number_input("Avg pages per PDF",   min_value=5,  max_value=500,  value=40)
    num_queries = col3.number_input("Queries per month",   min_value=10, max_value=5000, value=200)

    # Calculations
    total_pages   = num_pdfs * pages_each
    chars_per_page = 1800
    total_chars   = total_pages * chars_per_page
    total_chunks  = total_chars // 450          # avg chunk ~450 chars

    # OpenAI pricing (as of 2025)
    embed_tokens  = (total_chars / 4)           # ~4 chars per token
    embed_cost    = (embed_tokens / 1_000_000) * 0.02   # $0.02/1M tokens

    # GPT-4o-mini: $0.15/1M input, $0.60/1M output
    context_tokens_per_q = 5 * 500 / 4         # top-5 chunks
    input_tokens_month   = num_queries * (context_tokens_per_q + 50)
    output_tokens_month  = num_queries * 200
    gen_cost_month = (input_tokens_month / 1_000_000 * 0.15 +
                      output_tokens_month / 1_000_000 * 0.60)

    total_month = embed_cost + gen_cost_month

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Chunks",    f"{total_chunks:,}")
    col2.metric("Embedding Cost",  f"${embed_cost:.4f}",  delta="one-time")
    col3.metric("Generation/mo",   f"${gen_cost_month:.3f}")
    col4.metric("Total First Mo",  f"${total_month:.3f}",
                delta=f"~₹{total_month * 83:.0f}")

    st.caption("💡 Prices based on OpenAI 2025 rates: text-embedding-3-small ($0.02/1M), gpt-4o-mini ($0.15/$0.60 per 1M in/out)")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Setup Checklist ────────────────────────────────────────────────────
    st.markdown("### ✅ Setup Checklist")

    store_ok   = os.path.exists("vector_store/index.faiss")
    meta_ok    = os.path.exists("vector_store/metadata.json")
    pdf_ok     = os.path.exists("pdfs") and len(os.listdir("pdfs")) > 0 if os.path.exists("pdfs") else False
    api_key_ok = bool(st.session_state.get("api_key") or os.environ.get("OPENAI_API_KEY"))

    def check(ok, label, fix):
        icon  = "✅" if ok else "❌"
        color = "#00C49A" if ok else "#F85149"
        note  = "" if ok else f'<span style="color:#8B949E;font-size:0.75rem;"> → {fix}</span>'
        st.markdown(
            f'<div style="padding:6px 0; font-size:0.85rem;">'
            f'<span style="color:{color}">{icon}</span> {label}{note}</div>',
            unsafe_allow_html=True
        )

    check(pdf_ok,     "PDFs present in `pdfs/` folder",       "Add your PDF files to the pdfs/ directory")
    check(store_ok,   "FAISS index built (`vector_store/`)",   "Run: `python main.py`")
    check(meta_ok,    "Metadata file exists",                  "Run: `python main.py`")
    check(api_key_ok, "OpenAI API key configured",             "Add key in sidebar or set OPENAI_API_KEY env var")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── FAQ ────────────────────────────────────────────────────────────────
    st.markdown("### ❓ FAQ")

    faqs = [
        ("Why does the answer say 'not found in context'?",
         "The relevant chunk may not be in the top-k results. Try increasing the 'Chunks to retrieve' slider in the sidebar from 5 to 8–10."),
        ("How do I add new PDFs without re-embedding everything?",
         "Run `python embed_store.py --incremental` (or re-run the full pipeline). FAISS supports adding new vectors without rebuilding from scratch using `index.add()`."),
        ("Can I use GPT-4o instead of GPT-4o-mini?",
         "Yes — switch the model in the sidebar dropdown. GPT-4o gives better reasoning for complex financial questions but costs ~10x more per query."),
        ("What if my PDFs are scanned images (no text layer)?",
         "PyPDF2 can't extract text from scanned PDFs. Use `pytesseract` + `pdf2image` for OCR before the parsing step."),
        ("How accurate are the similarity scores?",
         "Scores range 0–1 (cosine similarity). Above 0.85 = strong match, 0.70–0.85 = relevant, below 0.70 = weak. You can filter low-score chunks in `rag_query.py`."),
        ("Can I host this for free?",
         "Yes — deploy on Streamlit Cloud (free tier). Push your repo to GitHub, connect at share.streamlit.io, and add your OPENAI_API_KEY as a secret."),
    ]

    for question, answer in faqs:
        with st.expander(f"🔹 {question}"):
            st.markdown(f'<div style="color:#8B949E; font-size:0.85rem; line-height:1.7;">{answer}</div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:1.5rem; border-top:1px solid #21262D; 
                color:#484F58; font-size:0.75rem; margin-top:1rem;">
        FinRAG · Financial Document Intelligence · Built with OpenAI + FAISS + Streamlit<br>
        <span style="color:#00C49A;">text-embedding-3-small</span> · 
        <span style="color:#00C49A;">gpt-4o-mini</span> · 
        <span style="color:#00C49A;">FAISS IndexFlatIP</span>
    </div>
    """, unsafe_allow_html=True)