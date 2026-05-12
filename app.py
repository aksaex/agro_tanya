# --- HACK WAJIB UNTUK STREAMLIT CLOUD ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ----------------------------------------

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌾", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@400;500;600&display=swap');

    /* ── RESET & BASE ── */
    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif !important;
        background-color: #F7F0E6 !important;
        color: #2A1F14 !important;
    }
    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 0 0 3rem !important;
        max-width: 700px !important;
        margin: 0 auto !important;
    }

    /* ── HERO — gelap hijau tua ── */
    .hero-wrap {
        background: #122A1A;
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -10%, rgba(45,122,58,0.45) 0%, transparent 70%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%232d7a3a' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        padding: 3rem 2rem 2.5rem;
        text-align: center;
        border-radius: 0 0 28px 28px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-wrap::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 0; right: 0;
        height: 28px;
        background: #F7F0E6;
        border-radius: 28px 28px 0 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        color: #A8D4A8;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        border-radius: 50px;
        border: 1px solid rgba(168,212,168,0.3);
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-family: 'Lora', Georgia, serif !important;
        font-size: 3rem !important;
        font-weight: 600 !important;
        color: #F5EFDF !important;
        margin: 0 0 0.5rem !important;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .hero-title span {
        color: #6EC97E;
    }
    .hero-divider {
        width: 40px;
        height: 2px;
        background: rgba(110,201,126,0.6);
        margin: 0.9rem auto;
        border-radius: 2px;
    }
    .hero-subtitle {
        color: rgba(245,239,223,0.65);
        font-size: 0.9rem;
        line-height: 1.65;
        margin: 0;
        max-width: 400px;
        margin-inline: auto;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.8rem;
    }
    .hero-stat {
        text-align: center;
    }
    .hero-stat-num {
        font-family: 'Lora', serif;
        font-size: 1.35rem;
        font-weight: 600;
        color: #6EC97E;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 0.68rem;
        color: rgba(245,239,223,0.45);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 0.2rem;
    }

    /* ── CONTENT AREA ── */
    .content-wrap {
        padding: 0 1.5rem;
    }

    /* ── FORM AREA ── */
    div[data-testid="stForm"] {
        background: #FFFDF7 !important;
        padding: 1.2rem 1.25rem 1rem !important;
        border-radius: 18px !important;
        border: 1px solid #DDD3BE !important;
        box-shadow: 0 2px 12px rgba(42,31,20,0.07) !important;
        margin-bottom: 1.5rem !important;
    }

    /* Label di atas input */
    .stTextInput label {
        font-weight: 600 !important;
        color: #3A2A18 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }

    /* Input field */
    .stTextInput > div > div > input {
        background-color: #F7F0E6 !important;
        border: 1.5px solid #C9BC9A !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        color: #2A1F14 !important;
        transition: border-color 0.15s, box-shadow 0.15s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2D7A3A !important;
        box-shadow: 0 0 0 3px rgba(45,122,58,0.14) !important;
        background-color: #FFFDF7 !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #B5A888 !important;
        font-style: italic;
    }

    /* Tombol — rata bawah dengan input */
    .stButton > button {
        background: linear-gradient(135deg, #2D7A3A 0%, #1B5228 100%) !important;
        color: #F5EFDF !important;
        border: none !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 46px !important;
        padding: 0 !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        margin-top: 1.65rem !important;
        transition: opacity 0.15s, transform 0.1s, box-shadow 0.15s !important;
        box-shadow: 0 3px 10px rgba(27,82,40,0.3) !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 14px rgba(27,82,40,0.35) !important;
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* ── RESPONS AI ── */
    .ai-response {
        background: #FFFDF7;
        border-radius: 18px;
        padding: 1.5rem 1.6rem;
        border: 1px solid #DDD3BE;
        border-left: 4px solid #2D7A3A;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 14px rgba(42,31,20,0.07);
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1rem;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid #EDE5D4;
    }
    .ai-avatar {
        background: linear-gradient(135deg, #1B5228, #2D7A3A);
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-size: 1.05rem;
        flex-shrink: 0;
        box-shadow: 0 2px 6px rgba(27,82,40,0.25);
    }
    .ai-meta { flex: 1; }
    .ai-name {
        font-weight: 600;
        color: #1A3A1A;
        font-size: 0.88rem;
        margin: 0;
        line-height: 1.2;
    }
    .ai-role {
        font-size: 0.73rem;
        color: #7A8E6A;
        margin: 0;
    }
    .ai-content {
        color: #3A2A18;
        line-height: 1.8;
        font-size: 0.94rem;
    }

    /* ── REFERENSI ── */
    .ref-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #7A6A50;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ref-section-title::before {
        content: '';
        display: inline-block;
        width: 18px;
        height: 2px;
        background: #B5A070;
        border-radius: 2px;
    }
    .ref-card {
        background: #FFFDF7;
        border-radius: 14px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
        border: 1px solid #DDD3BE;
        box-shadow: 0 1px 5px rgba(42,31,20,0.05);
        transition: border-color 0.15s;
    }
    .ref-card:hover {
        border-color: #A8C0A0;
    }
    .ref-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #1B4D2E;
        margin-bottom: 0.45rem;
        display: flex;
        align-items: flex-start;
        gap: 0.45rem;
    }
    .ref-num {
        background: #122A1A;
        color: #6EC97E;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 5px;
        flex-shrink: 0;
        margin-top: 1px;
        letter-spacing: 0.3px;
    }
    .ref-text {
        font-size: 0.82rem;
        line-height: 1.65;
        color: #5A4A38;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding: 1.25rem 1.5rem;
        background: #122A1A;
        border-radius: 16px;
        color: rgba(245,239,223,0.45);
        font-size: 0.76rem;
        line-height: 1.7;
    }
    .footer strong { color: #6EC97E; font-weight: 600; }

    /* ── SPINNER ── */
    .stSpinner > div > div { border-top-color: #2D7A3A !important; }

    /* ── MOBILE ── */
    @media (max-width: 600px) {
        .hero-wrap { padding: 2.25rem 1.25rem 2rem; border-radius: 0 0 20px 20px; }
        .hero-title { font-size: 2.2rem !important; }
        .hero-stats { gap: 1.25rem; }
        .block-container { padding: 0 0 2rem !important; }
        .content-wrap { padding: 0 0.85rem; }
        .ai-response { padding: 1.1rem 1.1rem; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP GEMINI API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Kunci API Gemini belum dipasang di Secrets Streamlit.")
    st.stop()

# 3. LOAD DATABASE
@st.cache_resource(show_spinner="Menginisialisasi database jurnal...")
def load_system():
    db_path = "./agro_tanya_db"
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")

    if os.path.exists(sqlite_file):
        file_size = os.path.getsize(sqlite_file)
        if file_size < 1000:
            st.error(f"Database rusak: file hanya {file_size} bytes (Git LFS pointer).")
            st.info("Solusi: hapus app di Streamlit Cloud lalu buat ulang agar file 217MB terunduh.")
            st.stop()
    else:
        st.error(f"Database tidak ditemukan: {sqlite_file}")
        st.stop()

    client = chromadb.PersistentClient(path=db_path)
    available_collections = [c.name for c in client.list_collections()]
    target_collection = "agro_tanya_padi_jagung"

    if target_collection not in available_collections:
        st.error(f"Koleksi tidak ditemukan. Koleksi tersedia: {available_collections}")
        st.stop()

    collection = client.get_collection(name=target_collection)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model, collection

model, collection = load_system()

# 4. UI — HERO
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">36.000+ Jurnal Akademis Terindeks</div>
    <h1 class="hero-title">AGRO<span>·TANYA</span></h1>
    <div class="hero-divider"></div>
    <p class="hero-subtitle">Asisten penyuluh virtual untuk hama, penyakit, dan budidaya Padi & Jagung di Sulawesi Selatan.</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">36K+</div>
            <div class="hero-stat-label">Jurnal</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">2</div>
            <div class="hero-stat-label">Komoditas</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">RAG</div>
            <div class="hero-stat-label">Teknologi</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. FORM — tombol inline di sebelah kanan input
with st.form(key='chat_form'):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "PERTANYAAN ANDA",
            placeholder="Contoh: Daun jagung menguning dan bule, apa solusinya?",
        )
    with col_btn:
        submit_button = st.form_submit_button(label="➤")

# 6. LOGIKA PENCARIAN
if submit_button and query:
    with st.spinner("Memindai jurnal..."):
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber Jurnal')}] {doc}\n\n"

    with st.spinner("Menyusun jawaban..."):
        prompt = f"""
        Anda adalah "Penyuluh Pintar", seorang ahli agronomi dan penyuluh pertanian lapangan asli Sulawesi Selatan (fokus Parepare & Sidrap) yang sangat berpengalaman, praktis, dan ramah. Anda melayani petani secara langsung melalui platform AGRO-TANYA.

        TUGAS UTAMA: 
        Jawab pertanyaan atau keluhan petani dengan akurat, ringkas, dan solutif HANYA berdasarkan fakta dari [REFERENSI JURNAL] di bawah.

        ATURAN KETAT (SYSTEM INSTRUCTIONS):
        1. SEMBUNYIKAN IDENTITAS AI (CRITICAL): DILARANG KERAS menyebut diri Anda sebagai AI, model bahasa, atau bot. DILARANG menggunakan kalimat pembuka/penutup template AI seperti "Tentu, saya bisa membantu", "Berikut adalah...", "Menurut referensi yang diberikan...", atau "Berdasarkan teks di atas...". Langsung jawab ke intinya selayaknya manusia yang sedang berbicara tatap muka.
        2. GAYA BAHASA & LOGAT (NATURAL): Gunakan Bahasa Indonesia yang profesional namun merakyat. Sisipkan sapaan dan partikel lokal Bugis-Makassar dengan natural dan tidak berlebihan (misal: "Tabe' Daeng", "iye'", "ki'", "pale'", "di'"). 
        3. ANTI-HALUSINASI (STRICT RAG): Jika informasi untuk menjawab pertanyaan TIDAK TERDAPAT di dalam [REFERENSI JURNAL], Anda DILARANG KERAS mengarang jawaban atau menebak-nebak. Cukup katakan persis seperti ini: "Tabe' Daeng, mohon maaf ki' pale', informasi spesifik mengenai hal tersebut kebetulan belum ada di catatan jurnal penyuluhan saya saat ini."
        4. PENANGANAN SAPAAN PENDEK: Jika input hanya berupa sapaan ("halo", "pagi", "assalamualaikum", "tes"), balas sapaan tersebut dengan sopan dan tanyakan kondisi tanaman padi/jagungnya hari ini. Abaikan referensi jurnal.
        5. FORMAT JAWABAN (HUMAN-LIKE): Jangan terlalu sering menggunakan list/bullet-points yang kaku. Ubah gaya penjelasan menjadi narasi 2-3 paragraf pendek yang luwes, mengalir, dan memberikan solusi yang bisa langsung dipraktikkan petani.

        [PERTANYAAN PETANI]: 
        "{query}"

        [REFERENSI JURNAL]:
        {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Maaf ki', jawaban tidak dapat ditampilkan."

            st.markdown(f"""
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">🌾</div>
                    <div class="ai-meta">
                        <p class="ai-name">Penyuluh Pintar</p>
                        <p class="ai-role">Ahli Agronomi · Sulawesi Selatan</p>
                    </div>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    st.markdown('<div class="ref-section-title">Sumber Jurnal</div>', unsafe_allow_html=True)

    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        judul = meta.get('Judul', 'Jurnal Akademis')

        st.markdown(f"""
        <div class="ref-card">
            <div class="ref-title">
                <span class="ref-num">{i+1}</span>
                {judul}
            </div>
            <div class="ref-text">{doc}</div>
        </div>
        """, unsafe_allow_html=True)

# 7. FOOTER
st.markdown("""
<div class="footer">
    <strong>AGRO-TANYA</strong> &nbsp;·&nbsp; Mata Kuliah Information Retrieval<br>
    ChromaDB &nbsp;·&nbsp; Google Gemini Flash &nbsp;·&nbsp; SentenceTransformers
</div>
""", unsafe_allow_html=True)