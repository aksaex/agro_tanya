# --- HACK WAJIB UNTUK STREAMLIT CLOUD ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ----------------------------------------

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌱", layout="centered")

# --- CSS KHUSUS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
    :root { --soil: #2C1A0E; --bark: #4A2C17; --moss: #3A5A2C; --leaf: #5C8A3C; --sprout: #7DB55A; --lime: #A8D87A; --cream: #FAF7F0; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; background-color: var(--cream) !important; color: var(--soil) !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 780px !important; margin: 0 auto !important; }
    .agro-hero { background: linear-gradient(160deg, var(--soil) 0%, var(--bark) 40%, var(--moss) 100%); padding: 48px 40px 36px; border-radius: 0 0 32px 32px; margin-bottom: 36px; }
    .hero-badge { display: inline-block; background: rgba(168,216,122,0.18); border: 1px solid rgba(168,216,122,0.35); color: var(--lime); font-size: 11px; font-weight: 600; letter-spacing: 2.5px; padding: 5px 14px; border-radius: 20px; margin-bottom: 14px; }
    .hero-title { font-family: 'Playfair Display', serif !important; font-size: 48px !important; font-weight: 900 !important; color: var(--cream) !important; margin: 0 0 10px !important; }
    .hero-title span { color: var(--lime); }
    .hero-sub { color: rgba(232,245,216,0.70); font-size: 15px; font-weight: 300; margin: 0; line-height: 1.6; }
    .stTextInput > div > div > input { border: 2px solid #d4e8c0 !important; border-radius: 14px !important; padding: 14px 18px !important; font-size: 15px !important; box-shadow: 0 2px 12px rgba(44,26,14,0.06) !important; }
    .stButton>button { background-color: var(--leaf); color: white; border-radius: 12px; padding: 10px 24px; font-weight: 600; width: 100%; border: none; margin-top: -10px;}
    .stButton>button:hover { background-color: var(--moss); box-shadow: 0 4px 12px rgba(92,138,60,0.3); color: white;}
    .answer-card { margin: 0 32px 15px; background: white; border-radius: 20px 20px 0 0; border: 1.5px solid #d4e8c0; border-bottom: none; }
    .answer-header { background: linear-gradient(135deg, var(--moss) 0%, var(--leaf) 100%); padding: 16px 22px; display: flex; align-items: center; gap: 10px; }
    .answer-header-icon { width: 36px; height: 36px; background: rgba(255,255,255,0.18); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .answer-header-text { color: white !important; font-size: 13px !important; font-weight: 600 !important; margin: 0 !important; }
    .gemini-response-box { margin: 0 32px 28px; padding: 22px 24px; background: white; border-radius: 0 0 20px 20px; border: 1.5px solid #d4e8c0; border-top: none; box-shadow: 0 8px 32px rgba(44,26,14,0.08); font-size: 15px; line-height: 1.75; }
    .ref-section { margin: 0 32px 36px; }
    .ref-section-title { font-size: 11px !important; font-weight: 700 !important; color: #8aaa70 !important; margin-bottom: 14px !important; }
    .ref-card { background: white; border: 1.5px solid #e4eedd; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; position: relative; }
    .ref-number { position: absolute; top: -10px; left: 16px; background: var(--leaf); color: white; font-size: 11px; font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .ref-source { font-size: 11px; font-weight: 700; color: var(--leaf); margin-bottom: 7px; }
    @media screen and (max-width: 768px) { .agro-hero { padding: 30px 20px 20px; border-radius: 0 0 20px 20px; margin-bottom: 24px; } .hero-title { font-size: 32px !important; } .answer-card, .gemini-response-box, .ref-section { margin-left: 15px; margin-right: 15px; } }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP GEMINI API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("⚠️ Kunci API Gemini belum dipasang di pengaturan rahasia (Secrets) Streamlit!")
    st.stop()

# 3. LOAD AI PUSTAKAWAN & DATABASE FISIK
@st.cache_resource(show_spinner="📥 Membuka rak database 36.000 Jurnal Kementan...")
def load_system():
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    # LANGSUNG BACA FOLDER DATABASE DARI GITHUB
    client = chromadb.PersistentClient(path="./agro_tanya_db")
    collection = client.get_collection(name="agro_tanya_padi_jagung")
    return model, collection

model, collection = load_system()

# 4. UI TAMPILAN
st.markdown("""
<div class="agro-hero">
    <div class="hero-badge">🌿 36.000+ Paragraf Jurnal & Pedoman</div>
    <div class="hero-title">AGRO<span>·</span>TANYA</div>
    <p class="hero-sub">Konsultasi hama, penyakit, dan perawatan<br>Padi & Jagung didukung AI — gratis untuk petani.</p>
</div>
""", unsafe_allow_html=True)

with st.form(key='chat_form'):
    query = st.text_input(
        "PERTANYAAN ANDA",
        placeholder="Contoh: Daun jagung saya bule dan menguning, obatnya apa pale'?",
    )
    submit_button = st.form_submit_button(label="Tanyakan ke Penyuluh Pintar 🚀")

# --- LOGIKA PENCARIAN ---
if submit_button and query:
    with st.spinner("🔍 Membaca 36.000+ dokumen jurnal..."):
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber')}] {doc}\n\n"

    with st.spinner("🤖 Menyusun jawaban ala Penyuluh Sulawesi..."):
        prompt = f"""
        Kamu adalah "Penyuluh Pintar", asisten virtual pertanian dari aplikasi AGRO-TANYA.
        Tugasmu membantu petani di Sulawesi Selatan (Parepare, Sidrap) untuk komoditas Padi dan Jagung.

        INSTRUKSI SANGAT KETAT (WAJIB DIIKUTI):
        1. Jika pertanyaan petani HANYA BERUPA SAPAAN (contoh: "hai", "halo", "assalamualaikum", "pagi"), maka BALAS SAPAAN TERSEBUT SAJA dengan ramah menggunakan logat Sulawesi Selatan (tabe', iye', ki', pale'). JANGAN berikan penjelasan pertanian apapun.
        2. Jika pertanyaan petani BUKAN sapaan (melainkan masalah pertanian), kamu WAJIB menjawab HANYA BERDASARKAN "REFERENSI KEMENTAN" di bawah ini.
        3. JIKA REFERENSI KEMENTAN TIDAK SESUAI dengan pertanyaan petani, JANGAN MENGARANG JAWABAN! Katakan saja: "Maaf ki' pale', informasi tentang hal itu belum ada di buku referensi jurnal saya saat ini."
        4. Selalu gunakan Bahasa Indonesia yang dicampur logat lokal Sulawesi Selatan yang natural dan sopan.

        Pertanyaan Petani: "{query}"
        
        REFERENSI KEMENTAN:
        {referensi_teks}
        """

        try:
            response = gemini_model.generate_content(prompt)
            jawaban_ai = response.text if response.parts else "Maaf ki', jawaban diblokir oleh sistem."

            st.markdown("""<div class="answer-card"><div class="answer-header"><div class="answer-header-icon">👨‍🌾</div><p class="answer-header-text">Penyuluh Pintar · AGRO-TANYA</p></div></div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="gemini-response-box">{jawaban_ai}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    # REFERENSI CARDS
    st.markdown('<div class="ref-section"><div class="ref-section-title">📚 &nbsp;Fakta Asli dari Database Jurnal & Kementan</div>', unsafe_allow_html=True)
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        judul = meta.get('Judul', 'Sumber Jurnal/Kementan')
        st.markdown(f"""
        <div class="ref-card">
            <div class="ref-number">{i+1}</div>
            <div class="ref-source">📖 &nbsp;{judul}</div>
            <div style="font-size: 13.5px; line-height: 1.65; color: #4a3a2e;">{doc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)