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

# --- CSS REVISI FINAL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: #F5F5F0 !important;
        color: #1A2E1A !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 2.5rem 1rem 3rem !important;
        max-width: 680px !important;
        margin: 0 auto !important;
    }

    /* ── HERO ── */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2.5rem 1.5rem 2rem;
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid #D6E8D6;
    }
    .hero-badge {
        display: inline-block;
        background: #D6E8D6;
        color: #1B4D2E;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        padding: 0.35rem 0.9rem;
        border-radius: 50px;
        margin-bottom: 1.1rem;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 2.6rem !important;
        font-weight: 400 !important;
        color: #1A2E1A !important;
        margin: 0 0 0.6rem !important;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .hero-title span { color: #2D7A3A; }
    .hero-subtitle {
        color: #5A6E5A;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
        max-width: 440px;
        margin-inline: auto;
    }

    /* ── FORM ── */
    div[data-testid="stForm"] {
        background: #ffffff;
        padding: 1.25rem 1.25rem 1rem;
        border-radius: 20px;
        border: 1px solid #D6E8D6;
        margin-bottom: 1.5rem;
    }
    .stTextInput label {
        font-weight: 500 !important;
        color: #2D4A2D !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.3px;
    }
    .stTextInput > div > div > input {
        background-color: #F5F5F0 !important;
        border: 1px solid #C4D9C4 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        color: #1A2E1A !important;
        transition: border-color 0.15s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2D7A3A !important;
        box-shadow: 0 0 0 3px rgba(45, 122, 58, 0.12) !important;
        background-color: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9AAA9A !important;
    }

    /* ── TOMBOL KIRIM — IKON SAJA ── */
    .stButton > button {
        background-color: #2D7A3A !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        width: 48px !important;
        height: 48px !important;
        padding: 0 !important;
        font-size: 1.3rem !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0.4rem !important;
        transition: background-color 0.15s ease, transform 0.1s ease;
        float: right;
    }
    .stButton > button:hover {
        background-color: #1B5E27 !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: scale(0.96);
    }

    /* ── RESPONS AI ── */
    .ai-response {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        border: 1px solid #D6E8D6;
        border-left: 4px solid #2D7A3A;
        margin-bottom: 1.5rem;
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 1rem;
        padding-bottom: 0.9rem;
        border-bottom: 1px solid #EBF3EB;
    }
    .ai-avatar {
        background: #D6E8D6;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .ai-name {
        font-weight: 600;
        color: #1A2E1A;
        font-size: 0.88rem;
        margin: 0;
    }
    .ai-content {
        color: #2D4A2D;
        line-height: 1.75;
        font-size: 0.93rem;
    }

    /* ── REFERENSI ── */
    .ref-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: #5A6E5A;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }
    .ref-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
        border: 1px solid #D6E8D6;
    }
    .ref-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #1B4D2E;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: flex-start;
        gap: 0.4rem;
    }
    .ref-num {
        background: #D6E8D6;
        color: #1B4D2E;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .ref-text {
        font-size: 0.82rem;
        line-height: 1.6;
        color: #4A5E4A;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.25rem;
        border-top: 1px solid #D6E8D6;
        color: #8A9E8A;
        font-size: 0.78rem;
        line-height: 1.6;
    }
    .footer strong { color: #5A6E5A; }

    /* ── SPINNER ── */
    .stSpinner > div > div { border-top-color: #2D7A3A !important; }

    /* ── MOBILE RESPONSIVE ── */
    @media (max-width: 600px) {
        .block-container {
            padding: 1.25rem 0.75rem 2rem !important;
        }
        .hero-container {
            padding: 1.75rem 1rem 1.5rem;
            border-radius: 16px;
        }
        .hero-title {
            font-size: 2rem !important;
        }
        .hero-subtitle {
            font-size: 0.85rem;
        }
        div[data-testid="stForm"] {
            padding: 1rem !important;
            border-radius: 16px;
        }
        .ai-response {
            padding: 1.1rem 1rem;
            border-radius: 14px;
        }
        .ref-card {
            border-radius: 10px;
        }
        .stButton > button {
            width: 44px !important;
            height: 44px !important;
        }
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

# 4. UI
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">36.000+ Jurnal Akademis</div>
    <h1 class="hero-title">AGRO<span>·TANYA</span></h1>
    <p class="hero-subtitle">Asisten penyuluh virtual untuk hama, penyakit, dan budidaya Padi & Jagung di Sulawesi Selatan.</p>
</div>
""", unsafe_allow_html=True)

with st.form(key='chat_form'):
    query = st.text_input(
        "Pertanyaan",
        placeholder="Contoh: Daun jagung menguning dan bule, apa solusinya?",
        label_visibility="collapsed",
    )
    # Tombol ikon kirim (panah kanan)
    submit_button = st.form_submit_button(label="➤")

# --- LOGIKA PENCARIAN ---
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
                    <p class="ai-name">Penyuluh Pintar</p>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    st.markdown('<div class="ref-header">Sumber Jurnal</div>', unsafe_allow_html=True)

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

# FOOTER
st.markdown("""
<div class="footer">
    <strong>Mata Kuliah Information Retrieval</strong><br>
    ChromaDB &middot; Google Gemini Flash
</div>
""", unsafe_allow_html=True)