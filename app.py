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

# 1. KONFIGURASI HALAMAN (Wajib di baris pertama)
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌾", layout="centered")

# --- CSS MODERN STARTUP EDITION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #F8F9FA !important;
        color: #1F2937 !important;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 1rem !important;
        max-width: 720px !important;
        margin: 0 auto !important;
    }

    /* Hero Section Minimalist */
    .hero-container {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        border: 1px solid #F3F4F6;
    }
    .hero-badge {
        display: inline-block;
        background: #DEF7EC;
        color: #046C4E;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
        margin: 0 0 0.5rem !important;
        letter-spacing: -1px;
    }
    .hero-title span { color: #10B981; }
    .hero-subtitle {
        color: #6B7280;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }

    /* Chat Input Form */
    div[data-testid="stForm"] {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #E5E7EB;
        margin-bottom: 2rem;
    }
    .stTextInput label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600 !important;
        color: #374151 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stTextInput > div > div > input {
        background-color: #F9FAFB !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
        background-color: white !important;
    }
    
    /* Button Minimalist */
    .stButton>button {
        background-color: #10B981;
        color: white;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        border: none;
        transition: all 0.2s ease;
        margin-top: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #059669;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    /* AI Response Card */
    .ai-response {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #E5E7EB;
        margin-bottom: 2rem;
        border-left: 5px solid #10B981;
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F3F4F6;
    }
    .ai-avatar {
        background: #DEF7EC;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-size: 1.2rem;
    }
    .ai-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        color: #111827;
        font-size: 0.95rem;
        margin: 0;
    }
    .ai-content {
        color: #374151;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    /* Reference Section */
    .ref-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ref-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #E5E7EB;
        transition: all 0.2s ease;
    }
    .ref-card:hover {
        border-color: #D1D5DB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .ref-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #046C4E;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .ref-text {
        font-size: 0.85rem;
        line-height: 1.6;
        color: #4B5563;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E5E7EB;
        color: #9CA3AF;
        font-size: 0.8rem;
    }
    .footer strong { color: #6B7280; }
    
    /* Streamlit Spinner */
    .stSpinner > div > div { border-top-color: #10B981 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP GEMINI API (REKOMENDASI: gemini-1.5-flash)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("⚠️ Kunci API Gemini belum dipasang di pengaturan rahasia (Secrets) Streamlit!")
    st.stop()

# 3. LOAD AI PUSTAKAWAN & DATABASE FISIK
@st.cache_resource(show_spinner="📥 Menginisialisasi 36.000+ Jurnal Pertanian...")
def load_system():
    db_path = "./agro_tanya_db"
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")
    
    # Pengecekan Git LFS
    if os.path.exists(sqlite_file):
        file_size = os.path.getsize(sqlite_file)
        if file_size < 1000:
            st.error(f"⚠️ DATABASE RUSAK: Streamlit hanya membaca Pointer LFS ({file_size} bytes).")
            st.info("💡 Solusi: Harus 'Delete App' di Streamlit Cloud lalu 'Create New App' agar mendownload file 217MB yang asli.")
            st.stop()
    else:
        st.error(f"❌ DATABASE TIDAK DITEMUKAN: File {sqlite_file} tidak ada! Pastikan folder di-upload ke GitHub.")
        st.stop()

    client = chromadb.PersistentClient(path=db_path)
    available_collections = [c.name for c in client.list_collections()]
    target_collection = "agro_tanya_padi_jagung"
    
    if target_collection not in available_collections:
        st.error(f"❌ KOLEKSI TIDAK DITEMUKAN! Yang ada di databasemu: {available_collections}")
        st.stop()
        
    collection = client.get_collection(name=target_collection)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    return model, collection

model, collection = load_system()

# 4. UI TAMPILAN
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Database 36.000+ Jurnal Akademis</div>
    <h1 class="hero-title">AGRO<span>·</span>TANYA</h1>
    <p class="hero-subtitle">Asisten penyuluh virtual untuk analisis hama, penyakit, dan budidaya Padi & Jagung di wilayah Sulawesi Selatan.</p>
</div>
""", unsafe_allow_html=True)

with st.form(key='chat_form'):
    query = st.text_input(
        "Tanyakan Masalah Pertanian Anda",
        placeholder="Contoh: Daun jagung saya bule dan menguning, apa solusinya pale'?",
    )
    submit_button = st.form_submit_button(label="Analisis dengan AI 🚀")

# --- LOGIKA PENCARIAN ---
if submit_button and query:
    with st.spinner("🔍 Memindai puluhan ribu dokumen jurnal..."):
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber Jurnal')}] {doc}\n\n"

    with st.spinner("🤖 Menyusun kesimpulan akademis..."):
        prompt = f"""
        Kamu adalah "Penyuluh Pintar", asisten pakar agronomi dari AGRO-TANYA.
        Tugasmu membantu petani di Sulawesi Selatan (Parepare, Sidrap) berdasarkan literatur akademis.

        INSTRUKSI SANGAT KETAT:
        1. Jika input HANYA BERUPA SAPAAN (contoh: "hai", "halo", "assalamualaikum"), balas sapaan tersebut dengan ramah menggunakan logat Sulawesi Selatan (tabe', iye', ki', pale'). Jangan bahas pertanian.
        2. Jika input adalah masalah pertanian, kamu WAJIB menjawab HANYA BERDASARKAN "REFERENSI JURNAL" di bawah.
        3. JIKA REFERENSI JURNAL TIDAK MENJAWAB PERTANYAAN (Out of Context), katakan: "Maaf ki' pale', informasi tentang hal tersebut belum tersedia di dalam korpus jurnal saya saat ini."
        4. Gunakan Bahasa Indonesia yang profesional namun sisipkan sedikit sapaan lokal Sulawesi Selatan agar terasa dekat dengan petani.

        Pertanyaan Petani: "{query}"
        
        REFERENSI JURNAL:
        {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Maaf ki', jawaban diblokir oleh sistem."

            # Tampilkan Jawaban AI
            st.markdown(f"""
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">👨‍🌾</div>
                    <p class="ai-name">Penyuluh Pintar AI</p>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    # Tampilkan Sumber Referensi
    st.markdown('<div class="ref-header">📚 Literatur Jurnal yang Ditemukan</div>', unsafe_allow_html=True)
    
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        judul = meta.get('Judul', 'Sumber Jurnal Akademis')
        
        st.markdown(f"""
        <div class="ref-card">
            <div class="ref-title">
                <span style="background:#E5E7EB; color:#4B5563; padding:2px 8px; border-radius:4px; font-size:0.7rem; margin-right:6px;">{i+1}</span>
                {judul}
            </div>
            <div class="ref-text">{doc}</div>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    Dikembangkan untuk <strong>Mata Kuliah Information Retrieval</strong><br>
    Menggunakan <strong>ChromaDB</strong> & <strong>Google Gemini Flash</strong>
</div>
""", unsafe_allow_html=True)