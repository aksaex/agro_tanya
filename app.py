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
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

    /* ── GLOBAL ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: #FAF7F0 !important;
        color: #1A2E1A !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 0 !important;
        max-width: 680px !important;
        margin: 0 auto !important;
    }

    /* ── HERO — dark green banner ── */
    .hero-container {
        background: #1A3D2B;
        padding: 2.8rem 2rem 2.5rem;
        text-align: center;
        border-radius: 0 0 28px 28px;
        margin-bottom: 2rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        color: #C8E6C9;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        padding: 0.3rem 0.85rem;
        border-radius: 50px;
        border: 1px solid rgba(200, 230, 201, 0.3);
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-family: 'Lora', serif !important;
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        color: #F0FAF0 !important;
        margin: 0 0 0.7rem !important;
        letter-spacing: -0.5px;
        line-height: 1.05;
    }
    .hero-title span { color: #81C784; }
    .hero-subtitle {
        color: #A5C8A5;
        font-size: 0.88rem;
        line-height: 1.65;
        margin: 0 auto;
        max-width: 400px;
    }

    /* ── CONTENT AREA ── */
    .content-wrap {
        padding: 0 1.25rem 2.5rem;
    }

    /* ── FORM CARD ── */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        padding: 1.1rem 1.25rem 1rem !important;
        border-radius: 18px;
        border: 1px solid #D8E8D0;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 16px rgba(26, 61, 43, 0.06);
    }

    /* ── INPUT ── */
    .stTextInput > div > div > input {
        background-color: #F5F8F2 !important;
        border: 1.5px solid #C8DCC0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.93rem !important;
        color: #1A2E1A !important;
        font-family: 'DM Sans', sans-serif !important;
        height: 48px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2D7A3A !important;
        box-shadow: 0 0 0 3px rgba(45, 122, 58, 0.14) !important;
        background-color: #ffffff !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9AAA8E !important;
        font-style: italic;
    }
    .stTextInput label { display: none !important; }

    /* ── BUTTON — kirim, ikon panah, di samping input ── */
    /*
       Trik: kolom terakhir di dalam form diatur ke lebar fixed ~56px,
       tombol dibuat kotak 48×48 dan di-push ke bawah supaya sejajar input.
    */
    div[data-testid="stForm"] div[data-testid="column"]:last-child {
        flex: 0 0 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        padding-left: 6px !important;
        padding-right: 0 !important;
    }
    div[data-testid="stForm"] div[data-testid="column"]:first-child {
        flex: 1 1 auto !important;
        padding-right: 0 !important;
    }
    .stButton > button {
        background-color: #1A3D2B !important;
        color: #F0FAF0 !important;
        border: none !important;
        border-radius: 12px !important;
        width: 48px !important;
        height: 48px !important;
        min-height: 48px !important;
        padding: 0 !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0 !important;
        transition: background-color 0.15s ease, transform 0.1s ease;
    }
    .stButton > button:hover {
        background-color: #2D7A3A !important;
        transform: scale(1.05);
    }
    .stButton > button:active {
        transform: scale(0.95) !important;
    }
    /* Hilangkan teks, tampilkan hanya SVG arrow */
    .stButton > button p {
        font-size: 0 !important;
        line-height: 0 !important;
        margin: 0 !important;
    }
    .stButton > button::after {
        content: "";
        display: block;
        width: 20px;
        height: 20px;
        background-color: #F0FAF0;
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='22' y1='2' x2='11' y2='13'/%3E%3Cpolygon points='22 2 15 22 11 13 2 9 22 2'/%3E%3C/svg%3E");
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='22' y1='2' x2='11' y2='13'/%3E%3Cpolygon points='22 2 15 22 11 13 2 9 22 2'/%3E%3C/svg%3E");
        -webkit-mask-size: contain;
        mask-size: contain;
        -webkit-mask-repeat: no-repeat;
        mask-repeat: no-repeat;
        -webkit-mask-position: center;
        mask-position: center;
    }

    /* ── SPINNER ── */
    .stSpinner > div > div { border-top-color: #2D7A3A !important; }

    /* ── RESPONS AI ── */
    .ai-response {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        border: 1px solid #D8E8D0;
        border-left: 4px solid #1A3D2B;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 16px rgba(26, 61, 43, 0.05);
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.9rem;
        padding-bottom: 0.9rem;
        border-bottom: 1px solid #EEF5EE;
    }
    .ai-avatar {
        background: #1A3D2B;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        flex-shrink: 0;
        color: #C8E6C9;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0;
        font-family: 'Lora', serif;
    }
    .ai-name {
        font-family: 'Lora', serif;
        font-weight: 600;
        color: #1A3D2B;
        font-size: 0.9rem;
        margin: 0;
    }
    .ai-content {
        color: #2A3E2A;
        line-height: 1.78;
        font-size: 0.92rem;
    }

    /* ── REFERENSI ── */
    .ref-section { margin-top: 0.25rem; }
    .ref-header {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6A8A6A;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        margin-bottom: 0.7rem;
        padding-left: 2px;
    }
    .ref-card {
        background: #F5F9F2;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.65rem;
        border: 1px solid #D8E8D0;
    }
    .ref-title {
        font-size: 0.81rem;
        font-weight: 600;
        color: #1A3D2B;
        margin-bottom: 0.45rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        line-height: 1.4;
    }
    .ref-num {
        background: #1A3D2B;
        color: #C8E6C9;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .ref-text {
        font-size: 0.81rem;
        line-height: 1.62;
        color: #4A6A4A;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding: 1.25rem 1rem 0;
        border-top: 1px solid #D8E8D0;
        color: #8A9E8A;
        font-size: 0.76rem;
        line-height: 1.6;
    }
    .footer strong { color: #4A6A4A; }

    /* ── MOBILE ── */
    @media (max-width: 600px) {
        .hero-container {
            padding: 2.2rem 1.25rem 2rem;
            border-radius: 0 0 20px 20px;
        }
        .hero-title { font-size: 2.1rem !important; }
        .hero-subtitle { font-size: 0.84rem; }
        .content-wrap { padding: 0 0.85rem 2rem; }
        div[data-testid="stForm"] {
            padding: 0.9rem 0.9rem 0.8rem !important;
            border-radius: 14px;
        }
        .ai-response {
            padding: 1.1rem 1rem;
            border-radius: 14px;
        }
        .ref-card { border-radius: 10px; }
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
        st.error(f"Koleksi tidak ditemukan. Tersedia: {available_collections}")
        st.stop()

    collection = client.get_collection(name=target_collection)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model, collection

model, collection = load_system()

# 4. UI — HERO
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">36.000+ Jurnal Akademis</div>
    <h1 class="hero-title">AGRO<span>·TANYA</span></h1>
    <p class="hero-subtitle">Asisten penyuluh virtual untuk hama, penyakit, dan budidaya Padi & Jagung di Sulawesi Selatan.</p>
</div>
""", unsafe_allow_html=True)

# 5. FORM — input + tombol sejajar dalam satu baris
with st.form(key='chat_form'):
    col_input, col_btn = st.columns([9, 1])
    with col_input:
        query = st.text_input(
            "q",
            placeholder="Tanyakan masalah tanaman padi atau jagung kamu...",
            label_visibility="collapsed",
        )
    with col_btn:
        submit_button = st.form_submit_button(label="kirim")

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
                    <div class="ai-avatar">AT</div>
                    <p class="ai-name">Penyuluh Pintar</p>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    st.markdown('<div class="ref-section"><div class="ref-header">Sumber Jurnal</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <strong>Mata Kuliah Information Retrieval</strong> &middot; ChromaDB &middot; Google Gemini Flash
</div>
""", unsafe_allow_html=True)