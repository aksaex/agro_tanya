# --- HACK WAJIB UNTUK STREAMLIT CLOUD (AGAR CHROMADB TIDAK ERROR) ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -------------------------------------------------------------------

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌱", layout="centered")

# --- CSS KHUSUS (DENGAN FITUR MOBILE RESPONSIVE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --soil:       #2C1A0E;
        --bark:       #4A2C17;
        --moss:       #3A5A2C;
        --leaf:       #5C8A3C;
        --sprout:     #7DB55A;
        --lime:       #A8D87A;
        --dew:        #E8F5D8;
        --cream:      #FAF7F0;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--cream) !important;
        color: var(--soil) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 0 !important;
        max-width: 780px !important;
        margin: 0 auto !important;
    }

    .agro-hero {
        background: linear-gradient(160deg, var(--soil) 0%, var(--bark) 40%, var(--moss) 100%);
        padding: 48px 40px 36px;
        border-radius: 0 0 32px 32px;
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(168,216,122,0.18);
        border: 1px solid rgba(168,216,122,0.35);
        color: var(--lime);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 20px;
        margin-bottom: 14px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 48px !important;
        font-weight: 900 !important;
        color: var(--cream) !important;
        line-height: 1.08 !important;
        margin: 0 0 10px !important;
        letter-spacing: -1px;
    }
    .hero-title span { color: var(--lime); }
    .hero-sub { color: rgba(232,245,216,0.70); font-size: 15px; font-weight: 300; margin: 0; line-height: 1.6; }

    .input-wrap { padding: 0 32px 24px; }
    .stTextInput > div > div > input {
        border: 2px solid #d4e8c0 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        background: white !important;
        color: var(--soil) !important;
        box-shadow: 0 2px 12px rgba(44,26,14,0.06) !important;
    }
    .stTextInput > div > div > input:focus { border-color: var(--leaf) !important; }
    
    .agro-divider { height: 1px; background: linear-gradient(90deg, transparent, #c8ddb0, transparent); margin: 4px 32px 28px; }

    .answer-card { margin: 0 32px 28px; background: white; border-radius: 20px; border: 1.5px solid #d4e8c0; box-shadow: 0 8px 32px rgba(44,26,14,0.08); overflow: hidden; }
    .answer-header { background: linear-gradient(135deg, var(--moss) 0%, var(--leaf) 100%); padding: 16px 22px; display: flex; align-items: center; gap: 10px; }
    .answer-header-icon { width: 36px; height: 36px; background: rgba(255,255,255,0.18); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .answer-header-text { color: white !important; font-size: 13px !important; font-weight: 600 !important; margin: 0 !important; }
    .answer-body { padding: 22px 24px; font-size: 15px; line-height: 1.75; color: var(--soil); }

    .ref-section { margin: 0 32px 36px; }
    .ref-section-title { font-size: 11px !important; font-weight: 700 !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: #8aaa70 !important; margin-bottom: 14px !important; display: flex; align-items: center; gap: 7px; }
    .ref-card { background: white; border: 1.5px solid #e4eedd; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; position: relative; }
    .ref-number { position: absolute; top: -10px; left: 16px; background: var(--leaf); color: white; font-size: 11px; font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .ref-source { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--leaf); margin-bottom: 7px; display: flex; align-items: center; gap: 5px; }
    .ref-text { font-size: 13.5px; line-height: 1.65; color: #4a3a2e; }

    .stSpinner > div > div { border-top-color: var(--leaf) !important; }
    .agro-footer { text-align: center; padding: 20px 32px 36px; font-size: 12px; color: #a0b890; line-height: 1.8; letter-spacing: 0.3px; }
    .agro-footer b { color: var(--leaf); }

    /* =========================================
       ✨ KODE RAHASIA AGAR RAPI DI HP (MOBILE)
       ========================================= */
    @media screen and (max-width: 768px) {
        .agro-hero { padding: 30px 20px 20px; border-radius: 0 0 20px 20px; margin-bottom: 24px; }
        .hero-title { font-size: 32px !important; }
        .hero-sub { font-size: 14px; }
        .input-wrap { padding: 0 15px 15px; }
        .answer-card { margin: 0 15px 20px; }
        .ref-section { margin: 0 15px 20px; }
        .answer-body { padding: 15px; font-size: 14px; }
        .ref-card { padding: 12px 15px; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP GEMINI API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("⚠️ Kunci API Gemini belum dipasang di pengaturan rahasia (Secrets) Streamlit!")
    st.stop()

# 3. LOAD AI PUSTAKAWAN & DATABASE (AUTO-SYNC DARI GOOGLE SHEETS)
@st.cache_resource(show_spinner="📥 Sedang menyinkronkan data terbaru dari Google Sheets...")
def load_system():
    # Load Otak AI
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # KITA GUNAKAN DATABASE IN-MEMORY (Bebas Error GitHub Corrupt!)
    client = chromadb.Client() 
    collection = client.create_collection(name="agro_tanya_padi_jagung")
    
    try:
        # Tarik data langsung dari Google Sheets
        sheet_url = "https://docs.google.com/spreadsheets/d/1ehA8R6kvitYumc1mb74VvfD026a3DQ5F1c1B85czpHE/export?format=csv&gid=1424564857"
        df = pd.read_csv(sheet_url)
        df.columns = [col.replace('[', '').replace(']', '').strip() for col in df.columns]
        
        kolom_teks = 'Isi Paragraf'
        if kolom_teks in df.columns:
            dokumen_teks = df[kolom_teks].astype(str).tolist()
            metadatas = df.to_dict(orient='records')
            
            for meta in metadatas:
                for key, value in meta.items():
                    meta[key] = str(value)
                    
            ids = [f"ID-{i}" for i in range(len(df))]
            
            # Ubah teks ke vektor lalu masukkan ke database memori
            embeddings = model.encode(dokumen_teks).tolist()
            collection.add(
                embeddings=embeddings,
                documents=dokumen_teks,
                metadatas=metadatas,
                ids=ids
            )
    except Exception as e:
        print("Gagal Sinkronisasi Google Sheets:", e)
        
    return model, collection

model, collection = load_system()

# 4. UI TAMPILAN
st.markdown("""
<div class="agro-hero">
    <div class="hero-badge">🌿 Berbasis Pedoman Kementan RI</div>
    <div class="hero-title">AGRO<span>·</span>TANYA</div>
    <p class="hero-sub">Konsultasi hama, penyakit, dan perawatan<br>Padi & Jagung didukung AI — gratis untuk petani.</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT ---
query = st.text_input(
    "PERTANYAAN ANDA",
    placeholder="Contoh: Daun jagung saya bule dan menguning, obatnya apa?",
)

st.markdown('<div class="agro-divider"></div>', unsafe_allow_html=True)

# --- LOGIKA PENCARIAN ---
if query:
    total_data = collection.count()
    
    # Pencegahan Error jika Google Sheet kosong/gagal terbaca
    if total_data == 0:
        st.error("⚠️ Sistem gagal membaca data dari Google Sheets. Pastikan link dapat diakses publik.")
    else:
        with st.spinner("🔍 Mencari referensi Kementan..."):
            query_vector = model.encode(query).tolist()
            
            # Ambil maksimal 3 hasil (atau kurang jika datanya sedikit)
            batas_hasil = min(3, total_data)
            results = collection.query(query_embeddings=[query_vector], n_results=batas_hasil)

            referensi_teks = ""
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                referensi_teks += f"- [{meta.get('Judul', 'Sumber')}] {doc}\n\n"

        with st.spinner("🤖 Merangkum jawaban untuk Anda..."):
            prompt = f"""
            Anda adalah asisten ahli pertanian bernama 'AGRO-TANYA'.
            Seorang petani bertanya: "{query}"
            
            TUGAS ANDA: Jawab pertanyaan tersebut HANYA berdasarkan referensi pedoman Kementan di bawah ini.
            Jangan mengarang informasi di luar referensi ini. Jika di referensi tidak ada jawabannya, bilang saja "Maaf, informasi tidak ditemukan di buku pedoman."
            Buat jawaban yang ramah, sopan, dan mudah dipahami petani. Gunakan pemformatan teks yang rapi.
            
            REFERENSI KEMENTAN:
            {referensi_teks}
            """

            try:
                response = gemini_model.generate_content(prompt)
                jawaban_ai = response.text if response.parts else "Maaf, jawaban diblokir oleh filter keamanan."

                st.markdown(f"""
                <div class="answer-card">
                    <div class="answer-header">
                        <div class="answer-header-icon">👨‍🌾</div>
                        <p class="answer-header-text">Jawaban AGRO-TANYA · AI Pertanian</p>
                    </div>
                    <div class="answer-body">

{jawaban_ai}

                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Gagal memanggil Gemini: {e}")

        # REFERENSI CARDS
        st.markdown('<div class="ref-section">', unsafe_allow_html=True)
        st.markdown('<div class="ref-section-title">📚 &nbsp;Fakta Asli dari Database Kementan</div>', unsafe_allow_html=True)

        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            judul = meta.get('Judul', 'Sumber Kementan')
            
            st.markdown(f"""
            <div class="ref-card">
                <div class="ref-number">{i+1}</div>
                <div class="ref-source">📖 &nbsp;{judul}</div>
                <div class="ref-text">

{doc}

                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="agro-footer">
    Didukung oleh <b>Google Gemini AI</b> · Data dari <b>Pedoman Kementan RI</b><br>
    Dibuat untuk membantu petani Indonesia 🇮🇩<br>
    <i>Proyek Mata Kuliah IR · Tim 6 Orang</i>
</div>
""", unsafe_allow_html=True)