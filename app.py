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
st.set_page_config(page_title="AGRO-TANYA | AI Agronomy Assistant", page_icon="🌱", layout="centered")

# --- CSS ENTERPRISE GRADE (RESPONSIF & MINIMALIS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Layout Responsif */
    .block-container {
        padding: 2rem 1rem !important;
        max-width: 768px !important;
        margin: 0 auto !important;
    }

    /* Minimalist Header */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .header-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #064E3B; /* Hijau Tua */
        letter-spacing: -0.025em;
        margin: 0 0 0.5rem 0;
    }
    .header-desc {
        font-size: 0.9rem;
        color: #6B7280;
        margin: 0;
        line-height: 1.5;
    }

    /* Chat Input Form (Merger Textbox & Tombol) */
    div[data-testid="stForm"] {
        border: none;
        background: transparent;
        padding: 0;
        box-shadow: none;
    }
    .stTextInput > div > div > input {
        border-radius: 24px !important;
        padding: 14px 20px !important;
        border: 1px solid #D1D5DB !important;
        font-size: 15px !important;
        background-color: #F9FAFB !important;
        transition: all 0.2s ease;
        padding-right: 50px !important; /* Ruang untuk tombol panah */
    }
    .stTextInput > div > div > input:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.1) !important;
        background-color: #FFFFFF !important;
    }
    
    /* Tombol Kirim Minimalis (Mirip ChatGPT) */
    .stButton>button {
        background-color: #059669;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        position: absolute;
        right: 5px;
        top: 2px; /* Disesuaikan agar sejajar dengan textbox */
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #047857;
        transform: scale(1.05);
    }
    /* Ganti teks tombol menjadi icon panah pakai CSS */
    .stButton>button p { display: none; }
    .stButton>button::after {
        content: "↑";
        font-size: 20px;
        font-weight: 600;
    }

    /* AI Response Card */
    .response-wrapper {
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid #E5E7EB;
    }
    .response-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .response-icon {
        background-color: #059669;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
    }
    .response-title {
        font-weight: 600;
        font-size: 14px;
        color: #374151;
        margin: 0;
    }
    .response-body {
        font-size: 15px;
        color: #1F2937;
        line-height: 1.6;
    }

    /* Source Reference section */
    .ref-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9CA3AF;
        margin-bottom: 12px;
        display: block;
    }
    .ref-item {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .ref-title {
        font-size: 13px;
        font-weight: 600;
        color: #064E3B;
        margin-bottom: 4px;
    }
    .ref-snippet {
        font-size: 13px;
        color: #6B7280;
        line-height: 1.5;
    }
    
    /* Penyesuaian khusus layar Android/Mobile */
    @media (max-width: 640px) {
        .block-container { padding: 1.5rem 1rem !important; }
        .header-title { font-size: 1.5rem; }
        .stTextInput > div > div > input { font-size: 16px !important; } /* Mencegah auto-zoom di iOS */
    }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Sistem membutuhkan API Key untuk beroperasi.")
    st.stop()

# 3. INISIALISASI DATABASE VEKTOR
@st.cache_resource(show_spinner="Menghubungkan ke basis data...")
def load_system():
    db_path = "./agro_tanya_db"
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")
    
    if os.path.exists(sqlite_file):
        if os.path.getsize(sqlite_file) < 1000:
            st.error("Integritas data terganggu. Silakan hubungi administrator.")
            st.stop()
    else:
        st.error("Basis data tidak ditemukan.")
        st.stop()

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="agro_tanya_padi_jagung")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    return model, collection

model, collection = load_system()

# 4. ANTARMUKA PENGGUNA (UI)
st.markdown("""
<div class="header-container">
    <h1 class="header-title">AGRO-TANYA</h1>
    <p class="header-desc">Asisten Agronomi Pintar. Didukung oleh 36.000 literatur akademis.</p>
</div>
""", unsafe_allow_html=True)

# Membungkus Input dan Tombol agar sejajar (Teknik CSS Hack)
with st.container():
    st.markdown('<div style="position: relative;">', unsafe_allow_html=True)
    with st.form(key='chat_form', clear_on_submit=False):
        # Kolom ini kita akali dengan CSS absolut agar tombol masuk ke dalam baris teks
        query = st.text_input(
            "label_hidden",
            label_visibility="collapsed",
            placeholder="Tanyakan masalah pertanian Anda...",
        )
        submit_button = st.form_submit_button(label="Kirim")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. LOGIKA SISTEM RAG
if submit_button and query:
    with st.spinner("Menganalisis literatur..."):
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber Literatur')}] {doc}\n\n"

    with st.spinner("Memproses respon..."):
        prompt = f"""
        Anda adalah asisten pakar agronomi lapangan (fokus wilayah Parepare, Sulawesi Selatan).
        
        INSTRUKSI KETAT:
        1. Jawab pertanyaan pengguna HANYA berdasarkan [REFERENSI JURNAL] di bawah ini.
        2. Jika informasi TIDAK ADA di referensi, sampaikan dengan sopan bahwa data spesifik belum tersedia di korpus. DILARANG MENGARANG JAWABAN.
        3. Gunakan bahasa Indonesia baku namun praktis. Sesekali gunakan partikel Bugis-Makassar (misal: ki', iye') agar natural.
        4. Langsung ke inti jawaban tanpa basa-basi seperti "Berdasarkan referensi...".

        [PERTANYAAN PENGGUNA]: "{query}"
        [REFERENSI JURNAL]: {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Respon tidak dapat diproses."

            # TAMPILKAN JAWABAN
            st.markdown(f"""
            <div class="response-wrapper">
                <div class="response-header">
                    <div class="response-icon">AI</div>
                    <p class="response-title">Penyuluh Pintar</p>
                </div>
                <div class="response-body">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # TAMPILKAN REFERENSI
            st.markdown('<span class="ref-label">Sumber Literatur Terkait</span>', unsafe_allow_html=True)
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                st.markdown(f"""
                <div class="ref-item">
                    <div class="ref-title">{meta.get('Judul', 'Dokumen Akademis')}</div>
                    <div class="ref-snippet">{doc}</div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Terjadi kesalahan pada server AI.")