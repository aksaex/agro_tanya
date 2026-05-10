# --- HACK WAJIB UNTUK STREAMLIT CLOUD ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ----------------------------------------

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌱", layout="centered")

# --- CSS KHUSUS (MOBILE RESPONSIVE & FORM STYLING) ---
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

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; background-color: var(--cream) !important; color: var(--soil) !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 780px !important; margin: 0 auto !important; }

    .agro-hero { background: linear-gradient(160deg, var(--soil) 0%, var(--bark) 40%, var(--moss) 100%); padding: 48px 40px 36px; border-radius: 0 0 32px 32px; margin-bottom: 36px; position: relative; overflow: hidden; }
    .hero-badge { display: inline-block; background: rgba(168,216,122,0.18); border: 1px solid rgba(168,216,122,0.35); color: var(--lime); font-size: 11px; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 14px; }
    .hero-title { font-family: 'Playfair Display', serif !important; font-size: 48px !important; font-weight: 900 !important; color: var(--cream) !important; line-height: 1.08 !important; margin: 0 0 10px !important; letter-spacing: -1px; }
    .hero-title span { color: var(--lime); }
    .hero-sub { color: rgba(232,245,216,0.70); font-size: 15px; font-weight: 300; margin: 0; line-height: 1.6; }

    .stTextInput > div > div > input { border: 2px solid #d4e8c0 !important; border-radius: 14px !important; padding: 14px 18px !important; font-size: 15px !important; box-shadow: 0 2px 12px rgba(44,26,14,0.06) !important; }
    .stTextInput > div > div > input:focus { border-color: var(--leaf) !important; }
    
    .stButton>button { background-color: var(--leaf); color: white; border-radius: 12px; padding: 10px 24px; font-weight: 600; width: 100%; border: none; transition: all 0.3s ease; margin-top: -10px;}
    .stButton>button:hover { background-color: var(--moss); box-shadow: 0 4px 12px rgba(92,138,60,0.3); color: white;}

    .agro-divider { height: 1px; background: linear-gradient(90deg, transparent, #c8ddb0, transparent); margin: 20px 32px 28px; }

    .answer-card { margin: 0 32px 15px; background: white; border-radius: 20px 20px 0 0; border: 1.5px solid #d4e8c0; border-bottom: none; overflow: hidden; }
    .answer-header { background: linear-gradient(135deg, var(--moss) 0%, var(--leaf) 100%); padding: 16px 22px; display: flex; align-items: center; gap: 10px; }
    .answer-header-icon { width: 36px; height: 36px; background: rgba(255,255,255,0.18); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .answer-header-text { color: white !important; font-size: 13px !important; font-weight: 600 !important; margin: 0 !important; }
    
    .gemini-response-box { margin: 0 32px 28px; padding: 22px 24px; background: white; border-radius: 0 0 20px 20px; border: 1.5px solid #d4e8c0; border-top: none; box-shadow: 0 8px 32px rgba(44,26,14,0.08); font-size: 15px; line-height: 1.75; color: var(--soil); }

    .ref-section { margin: 0 32px 36px; }
    .ref-section-title { font-size: 11px !important; font-weight: 700 !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: #8aaa70 !important; margin-bottom: 14px !important; display: flex; align-items: center; gap: 7px; }
    .ref-card { background: white; border: 1.5px solid #e4eedd; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; position: relative; }
    .ref-number { position: absolute; top: -10px; left: 16px; background: var(--leaf); color: white; font-size: 11px; font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .ref-source { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--leaf); margin-bottom: 7px; display: flex; align-items: center; gap: 5px; }

    .stSpinner > div > div { border-top-color: var(--leaf) !important; }
    .agro-footer { text-align: center; padding: 20px 32px 36px; font-size: 12px; color: #a0b890; line-height: 1.8; letter-spacing: 0.3px; }
    .agro-footer b { color: var(--leaf); }

    @media screen and (max-width: 768px) {
        .agro-hero { padding: 30px 20px 20px; border-radius: 0 0 20px 20px; margin-bottom: 24px; }
        .hero-title { font-size: 32px !important; }
        .answer-card, .gemini-response-box, .ref-section { margin-left: 15px; margin-right: 15px; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. SETUP GEMINI API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    # Gunakan model yang masih ada limitnya
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ Kunci API Gemini belum dipasang di pengaturan rahasia (Secrets) Streamlit!")
    st.stop()

# 3. LOAD AI PUSTAKAWAN & DATABASE (AUTO-SYNC GOOGLE SHEETS - ANTI CORRUPT)
@st.cache_resource(show_spinner="📥 Sedang menyinkronkan data terbaru dari Google Sheets...")
def load_system():
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    # Menggunakan IN-MEMORY DATABASE agar tidak error karena file Github corrupt
    client = chromadb.Client() 
    collection = client.create_collection(name="agro_tanya_padi_jagung")
    
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1ehA8R6kvitYumc1mb74VvfD026a3DQ5F1c1B85czpHE/export?format=csv&gid=1424564857"
        df = pd.read_csv(sheet_url)
        df.columns = [col.replace('[', '').replace(']', '').strip() for col in df.columns]
        
        # Mencegah error 'nan'
        df = df.dropna(subset=['Isi Paragraf'])
        
        kolom_teks = 'Isi Paragraf'
        if kolom_teks in df.columns:
            dokumen_teks = df[kolom_teks].astype(str).tolist()
            metadatas = df.to_dict(orient='records')
            for meta in metadatas:
                for key, value in meta.items():
                    meta[key] = str(value)
                    
            ids = [f"ID-{i}" for i in range(len(df))]
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

# 4. UI TAMPILAN HERO
st.markdown("""
<div class="agro-hero">
    <div class="hero-badge">🌿 Berbasis Pedoman Kementan RI</div>
    <div class="hero-title">AGRO<span>·</span>TANYA</div>
    <p class="hero-sub">Konsultasi hama, penyakit, dan perawatan<br>Padi & Jagung didukung AI — gratis untuk petani.</p>
</div>
""", unsafe_allow_html=True)

# --- FORM INPUT ---
with st.form(key='chat_form'):
    query = st.text_input(
        "PERTANYAAN ANDA",
        placeholder="Contoh: Daun jagung saya bule dan menguning, obatnya apa pale'?",
    )
    submit_button = st.form_submit_button(label="Tanyakan ke Penyuluh Pintar 🚀")

st.markdown('<div class="agro-divider"></div>', unsafe_allow_html=True)

# --- LOGIKA PENCARIAN & QA ---
if submit_button and query:
    total_data = collection.count()
    
    if total_data == 0:
        st.error("⚠️ Sistem gagal membaca data dari Google Sheets.")
    else:
        with st.spinner("🔍 Membaca jutaan dokumen Kementan..."):
            query_vector = model.encode(query).tolist()
            batas_hasil = min(3, total_data)
            results = collection.query(query_embeddings=[query_vector], n_results=batas_hasil)

            referensi_teks = ""
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                if str(doc).lower() != "nan":
                    referensi_teks += f"- [{meta.get('Judul', 'Sumber')}] {doc}\n\n"

        with st.spinner("🤖 Menyusun jawaban ala Penyuluh Sulawesi..."):
            prompt = f"""
            Kamu adalah "Penyuluh Pintar", asisten virtual pertanian dari aplikasi AGRO-TANYA.
            Tugasmu membantu petani di Sulawesi Selatan (Parepare, Sidrap) untuk komoditas Padi dan Jagung.

            INSTRUKSI SANGAT KETAT (WAJIB DIIKUTI):
            1. Jika pertanyaan petani HANYA BERUPA SAPAAN (contoh: "hai", "halo", "assalamualaikum", "pagi"), maka BALAS SAPAAN TERSEBUT SAJA dengan ramah menggunakan logat Sulawesi Selatan (tabe', iye', ki', pale'). JANGAN berikan penjelasan pertanian apapun.
            2. Jika pertanyaan petani BUKAN sapaan (melainkan masalah pertanian), kamu WAJIB menjawab HANYA BERDASARKAN "REFERENSI KEMENTAN" di bawah ini.
            3. JIKA REFERENSI KEMENTAN TIDAK SESUAI dengan pertanyaan petani (contoh: petani tanya sawit, tapi referensi isinya jagung), JANGAN MENGARANG JAWABAN! Katakan saja: "Maaf ki' pale', informasi tentang hal itu belum ada di buku pedoman saya saat ini."
            4. Selalu gunakan Bahasa Indonesia yang dicampur logat lokal Sulawesi Selatan yang natural dan sopan.

            Pertanyaan Petani: "{query}"
            
            REFERENSI KEMENTAN:
            {referensi_teks}
            """

            try:
                response = gemini_model.generate_content(prompt)
                jawaban_ai = response.text if response.parts else "Maaf ki', jawaban diblokir oleh sistem keamanan."

                st.markdown("""
                <div class="answer-card">
                    <div class="answer-header">
                        <div class="answer-header-icon">👨‍🌾</div>
                        <p class="answer-header-text">Penyuluh Pintar · AGRO-TANYA</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f'<div class="gemini-response-box">{jawaban_ai}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Gagal memanggil Gemini: {e}")

        # REFERENSI CARDS
        st.markdown('<div class="ref-section">', unsafe_allow_html=True)
        st.markdown('<div class="ref-section-title">📚 &nbsp;Fakta Asli dari Database Kementan</div>', unsafe_allow_html=True)

        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            judul = meta.get('Judul', 'Sumber Kementan')
            
            if str(doc).lower() != "nan":
                st.markdown(f"""
                <div class="ref-card">
                    <div class="ref-number">{i+1}</div>
                    <div class="ref-source">📖 &nbsp;{judul}</div>
                    <div style="font-size: 13.5px; line-height: 1.65; color: #4a3a2e;">{doc}</div>
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