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
st.set_page_config(page_title="AGRO-TANYA | AI", page_icon="🌾", layout="centered")

# --- CSS REVISI: 50% HIJAU TUA & 50% CREAM HANGAT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    /* Background Utama: Putih Hangat / Cream yang ramah mata */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #F9F7F1 !important; /* Warna Cream Hangat */
        color: #163820 !important; /* Teks Hijau Tua Gelap */
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 2rem 1rem 3rem !important;
        max-width: 720px !important;
        margin: 0 auto !important;
    }

    /* ── TOMBOL KEMBALI KE BERANDA ── */
    .back-btn-container {
        margin-bottom: 1.5rem;
    }
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #163820; 
        font-size: 0.875rem;
        font-weight: 600;
        text-decoration: none;
        padding: 0.5rem 1rem;
        background-color: #EAE6DA; /* Cream lebih gelap untuk tombol */
        border: 1px solid #D1CBB8;
        border-radius: 9999px;
        transition: all 0.2s ease;
    }
    .back-btn:hover {
        background-color: #163820; 
        color: #F9F7F1;
        border-color: #163820;
    }

    /* ── HERO SECTION (50% HIJAU TUA) ── */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 2rem;
        padding: 3rem 1.5rem;
        background: #163820; /* Hijau Tua Solid */
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(22, 56, 32, 0.2);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(249, 247, 241, 0.15); /* Transparan Putih */
        color: #F9F7F1; /* Putih Cream */
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        margin-bottom: 1.25rem;
        border: 1px solid rgba(249, 247, 241, 0.3);
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #F9F7F1 !important; /* Putih Cream */
        margin: 0 0 0.75rem !important;
        letter-spacing: -0.02em;
        line-height: 1.1;
        text-align: center;
    }
    .hero-title span { color: #84D996; /* Hijau Terang Accent */ }
    
    /* Mengunci subtitle agar selalu di tengah pada Desktop maupun HP */
    .hero-subtitle {
        color: #C3D6C8 !important; /* Hijau Pudar */
        font-size: 1rem;
        line-height: 1.6;
        margin: 0 auto !important;
        max-width: 480px;
        text-align: center !important;
    }

    /* ── FORM PENCARIAN ── */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        padding: 1rem 1rem 0.75rem;
        border-radius: 20px;
        border: 1px solid #EAE6DA;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    .stTextInput label {
        display: none !important;
    }
    .stTextInput > div > div > input {
        background-color: #F9F7F1 !important;
        border: 1px solid #D1CBB8 !important;
        border-radius: 12px !important;
        padding: 0.875rem 1.25rem !important;
        font-size: 1rem !important;
        color: #163820 !important;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #163820 !important; 
        box-shadow: 0 0 0 4px rgba(22, 56, 32, 0.1) !important;
        background-color: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #8C998E !important; 
    }

    /* ── TOMBOL KIRIM ── */
    .stButton > button {
        background-color: #163820 !important; /* Hijau Tua */
        color: #F9F7F1 !important;
        border: none !important;
        border-radius: 12px !important;
        width: 52px !important;
        height: 52px !important;
        padding: 0 !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0.15rem !important;
        transition: all 0.2s ease;
        float: right;
        box-shadow: 0 4px 6px -1px rgba(22, 56, 32, 0.3);
    }
    .stButton > button:hover {
        background-color: #245834 !important; /* Hijau Sedikit Terang */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(22, 56, 32, 0.4);
    }

    /* ── RESPONS AI ── */
    .ai-response {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #EAE6DA;
        border-left: 5px solid #163820; /* Garis aksen hijau tua */
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F0EEE4;
    }
    .ai-avatar {
        background: #EAF0EC;
        color: #163820;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .ai-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        color: #163820;
        font-size: 1rem;
        margin: 0;
    }
    .ai-content {
        color: #2D4A36;
        line-height: 1.8;
        font-size: 0.95rem;
    }
    .ai-content p {
        margin-bottom: 1rem;
    }
    .ai-content p:last-child {
        margin-bottom: 0;
    }

    /* ── REFERENSI ── */
    .ref-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 800;
        color: #163820;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ref-header::after {
        content: "";
        flex-grow: 1;
        height: 1px;
        background: #D1CBB8;
    }
    .ref-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid #EAE6DA;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .ref-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
    }
    .ref-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 800;
        color: #163820;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        line-height: 1.4;
    }
    .ref-num {
        background: #EAF0EC;
        color: #163820;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .ref-text {
        font-size: 0.875rem;
        line-height: 1.7;
        color: #4A6B53;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #D1CBB8;
        color: #8C998E;
        font-size: 0.8rem;
        line-height: 1.6;
    }
    .footer strong { color: #4A6B53; }

    /* ── SPINNER ── */
    .stSpinner > div > div { border-top-color: #163820 !important; }

    /* ── MOBILE RESPONSIVE ── */
    @media (max-width: 600px) {
        .block-container {
            padding: 1.25rem 1rem 2rem !important;
        }
        .hero-container {
            padding: 2.5rem 1.25rem 2rem;
            border-radius: 20px;
        }
        .hero-title {
            font-size: 2rem !important;
        }
        div[data-testid="stForm"] {
            padding: 0.75rem !important;
        }
        .stButton > button {
            width: 48px !important;
            height: 48px !important;
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
@st.cache_resource(show_spinner="Menginisialisasi sistem pintar...")
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
    model = SentenceTransformer('BAAI/bge-m3')
    return model, collection

model, collection = load_system()

# 4. UI

# Tombol Kembali ke Beranda
st.markdown("""
<div class="back-btn-container">
    <a href="https://agrotanya.netlify.app/" target="_self" class="back-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
    </a>
</div>
""", unsafe_allow_html=True)

# Hero Section Terpusat (Flexbox)
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="m17 5-5-3-5 3"/><path d="m19 12-7-7-7 7"/><path d="m21 19-9-9-9 9"/></svg>
        Information Retrieval
    </div>
    <h1 class="hero-title">AGRO<span>-TANYA</span></h1>
    <p class="hero-subtitle">Asisten virtual pintar berbasis dokumen penyuluhan resmi untuk budidaya Padi & Jagung di Parepare.</p>
</div>
""", unsafe_allow_html=True)

with st.form(key='chat_form'):
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "Pertanyaan",
            placeholder="Halo petani parepare. Sebaiknya kita mulai dari mana?",
            label_visibility="collapsed",
        )
    with col2:
        # Tombol ikon kirim (panah kanan gaya material/modern)
        submit_button = st.form_submit_button(label="➤")

# --- LOGIKA PENCARIAN ---
if submit_button and query:
    with st.spinner("Mencari jawaban di database..."):
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=5)

        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber Jurnal')}] {doc}\n\n"

    with st.spinner("Menyintesis informasi..."):
        prompt = f"""
        Anda adalah "Penyuluh Pintar", seorang ahli agronomi lapangan asli Sulawesi Selatan (fokus Parepare) di platform AGRO-TANYA.
        Tugas Anda adalah membaca [DOKUMEN PENYULUHAN] yang diberikan, lalu mengekstrak jawabannya untuk membalas [PERTANYAAN PETANI].

        ATURAN KETAT SINTESIS RAG (RETRIEVAL-AUGMENTED GENERATION):
        1. GROUNDING FAKTUAL (CRITICAL): Seluruh dosis pupuk, nama hama, nama pestisida, dan langkah teknis HARUS 100% diambil dari [DOKUMEN PENYULUHAN]. DILARANG KERAS menambahkan pengetahuan eksternal Anda sendiri.
        2. PENANGANAN HALUSINASI: Jika pertanyaan petani TIDAK ADA hubungannya dengan isi [DOKUMEN PENYULUHAN] (misalnya dokumen membahas padi, tapi petani bertanya tentang tomat), Anda WAJIB menjawab: "Tabe' Daeng, mohon maaf, informasi spesifik mengenai hal tersebut belum ada di catatan jurnal penyuluhan saya saat ini."
        3. GAYA BAHASA (LOCALIZED): Sampaikan jawaban dalam format narasi 2-3 paragraf yang ramah, sopan, dan mudah dipahami petani awam. Gunakan sapaan "Tabe' Daeng" di awal, dan sisipkan sedikit partikel lokal (iye', ki', pale', di') secara natural.
        4. TANPA TEMPLATE AI: JANGAN PERNAH menyebut "Berdasarkan dokumen...", "Menurut referensi...", atau "Saya adalah AI". Langsung berikan saran teknis seolah Anda sedang mengobrol di sawah.
        5. PENANGANAN SAPAAN: Jika petani hanya menyapa ("Halo", "Pagi"), balas dengan ramah dan tanyakan apa masalah padi/jagungnya hari ini.

        [PERTANYAAN PETANI]: 
        "{query}"

        [DOKUMEN PENYULUHAN]:
        {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Maaf ki', jawaban tidak dapat ditampilkan."

            st.markdown(f"""
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 5.4 8 12 8 12s8-6.6 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>
                    </div>
                    <p class="ai-name">Penyuluh Pintar</p>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memanggil AI: {e}")

    st.markdown('<div class="ref-header">Sumber Referensi Dokumen (Ground Truth)</div>', unsafe_allow_html=True)

    # Tampilkan maksimal 3 referensi terbaik di UI agar tidak memenuhi layar
    max_display = min(3, len(results['documents'][0]))
    for i in range(max_display):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        judul = meta.get('Judul', 'Dokumen Teknis Pertanian')

        # Potong teks jika terlalu panjang agar UI tetap bersih
        doc_preview = doc if len(doc) < 250 else doc[:250] + "..."

        st.markdown(f"""
        <div class="ref-card">
            <div class="ref-title">
                <span class="ref-num">{i+1}</span>
                {judul}
            </div>
            <div class="ref-text">{doc_preview}</div>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <strong>AGRO-TANYA Engine</strong><br>
    Information Retrieval Pipeline &middot; Semantic Search
</div>
""", unsafe_allow_html=True)