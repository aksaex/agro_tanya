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

# --- CSS REVISI FINAL (WARM WHITE & DARK GREEN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

    /* TEMA WARNA PUTIH HANGAT (WARM WHITE) */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: #F9F8F4 !important; /* Putih Hangat yang nyaman di mata */
        color: #162B16 !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 2.5rem 1rem 3rem !important;
        max-width: 680px !important;
        margin: 0 auto !important;
    }

    /* ── HERO SECTION ── */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 1.5rem;
        background: transparent;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 2.8rem !important;
        font-weight: 400 !important;
        color: #1A331A !important; /* Hijau Tua */
        margin: 0 0 0.2rem !important;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .hero-title span { color: #2D7A3A; }
    
    /* ── FORM SEARCH BAR (KAPSUL) ── */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        padding: 0.4rem 0.4rem 0.4rem 1.2rem;
        border-radius: 50px;
        border: 2px solid #1A331A; /* Border Hijau Tua */
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(26, 51, 26, 0.08);
    }
    /* Menghilangkan border default dari text input agar menyatu dengan Form */
    .stTextInput > div > div > input {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem 0 !important;
        font-size: 1.05rem !important;
        color: #1A331A !important;
    }
    .stTextInput > div > div > input:focus {
        border: none !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #7A8C7A !important;
        font-style: italic;
    }

    /* ── TOMBOL KIRIM DALAM KOLOM ── */
    .stButton > button {
        background-color: #1A331A !important; /* Hijau Tua */
        color: #F9F8F4 !important;
        border: none !important;
        border-radius: 50px !important;
        width: 100% !important;
        height: 48px !important;
        font-size: 1.4rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: background-color 0.15s ease, transform 0.1s ease;
    }
    .stButton > button:hover {
        background-color: #2D7A3A !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: scale(0.96);
    }

    /* ── RESPONS AI ── */
    .ai-response {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #E2E8E2;
        border-left: 5px solid #1A331A; /* Aksen Hijau Tua */
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F0F4F0;
    }
    .ai-avatar {
        background: #1A331A;
        color: #F9F8F4;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-size: 1.1rem;
    }
    .ai-name {
        font-weight: 700;
        color: #1A331A;
        font-size: 0.95rem;
        margin: 0;
    }
    .ai-content {
        color: #2A402A;
        line-height: 1.7;
        font-size: 1rem;
    }

    /* ── REFERENSI ── */
    .ref-header {
        font-size: 0.8rem;
        font-weight: 700;
        color: #1A331A;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }
    .ref-card {
        background: #F4F5F2; /* Putih sedikit lebih gelap dari background */
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border: 1px solid #E2E8E2;
    }
    .ref-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #1A331A;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    .ref-text {
        font-size: 0.85rem;
        line-height: 1.6;
        color: #4A5E4A;
    }

    /* ── MOBILE RESPONSIVE ── */
    @media (max-width: 600px) {
        .block-container {
            padding: 1.5rem 0.8rem 2rem !important;
        }
        .hero-title {
            font-size: 2.2rem !important;
        }
        div[data-testid="stForm"] {
            padding: 0.3rem 0.3rem 0.3rem 1rem;
        }
        .stTextInput > div > div > input {
            font-size: 0.95rem !important;
        }
        .stButton > button {
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
@st.cache_resource(show_spinner="Menginisialisasi sistem...")
def load_system():
    db_path = "./agro_tanya_db"
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")

    if os.path.exists(sqlite_file):
        file_size = os.path.getsize(sqlite_file)
        if file_size < 1000:
            st.error("Database rusak.")
            st.stop()
    else:
        st.error("Database tidak ditemukan.")
        st.stop()

    client = chromadb.PersistentClient(path=db_path)
    available_collections = [c.name for c in client.list_collections()]
    target_collection = "agro_tanya_padi_jagung"

    if target_collection not in available_collections:
        st.error("Koleksi database tidak ditemukan.")
        st.stop()

    collection = client.get_collection(name=target_collection)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model, collection

model, collection = load_system()

# 4. UI
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">AGRO<span>·TANYA</span></h1>
</div>
""", unsafe_allow_html=True)

# Membuat Form dengan tombol di samping menggunakan st.columns
with st.form(key='chat_form', clear_on_submit=False):
    # Mengatur layout 5 bagian untuk teks, 1 bagian untuk tombol
    col1, col2 = st.columns([5, 1])
    
    with col1:
        query = st.text_input(
            "Pertanyaan",
            placeholder="Halo petani parepare. Sebaiknya kita mulai dari mana?",
            label_visibility="collapsed",
        )
    with col2:
        # Tombol panah langsung di dalam form sebelahan dengan input
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
        Anda adalah seorang penyuluh pertanian lapangan asli Sulawesi Selatan (fokus Parepare & Sidrap) yang sangat berpengalaman, praktis, dan ramah. 

        TUGAS UTAMA: 
        Jawab pertanyaan petani dengan akurat, ringkas, dan solutif HANYA berdasarkan fakta dari [REFERENSI JURNAL] di bawah.

        ATURAN KETAT:
        1. SEMBUNYIKAN IDENTITAS AI: DILARANG menyebut diri Anda sebagai AI atau bot. Langsung jawab layaknya manusia tatap muka.
        2. GAYA BAHASA: Gunakan Bahasa Indonesia profesional namun merakyat. Sisipkan sapaan lokal (misal: "Tabe' Daeng", "iye'", "ki'"). 
        3. ANTI-HALUSINASI: Jika info TIDAK ADA di referensi, DILARANG mengarang. Jawab: "Tabe' Daeng, mohon maaf, informasi mengenai hal tersebut belum ada di catatan jurnal penyuluhan saya saat ini."
        4. FORMAT JAWABAN: Buat narasi 2-3 paragraf pendek yang mengalir. Jangan terlalu kaku.

        [PERTANYAAN PETANI]: 
        "{query}"

        [REFERENSI JURNAL]:
        {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Maaf, jawaban tidak dapat ditampilkan."

            st.markdown(f"""
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">🌾</div>
                    <p class="ai-name">Penyuluh</p>
                </div>
                <div class="ai-content">{jawaban_ai}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal memuat jawaban: {e}")

    st.markdown('<div class="ref-header">Sumber Jurnal</div>', unsafe_allow_html=True)

    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        judul = meta.get('Judul', 'Jurnal Akademis')

        st.markdown(f"""
        <div class="ref-card">
            <div class="ref-title">
                {judul}
            </div>
            <div class="ref-text">{doc}</div>
        </div>
        """, unsafe_allow_html=True)