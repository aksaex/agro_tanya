# --- HACK WAJIB UNTUK STREAMLIT CLOUD (AGAR CHROMADB TIDAK ERROR) ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -------------------------------------------------------------------

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    .res-box { padding: 15px; border-radius: 10px; background-color: #f0f8ff; border-left: 5px solid #2e7d32; margin-bottom: 10px; font-size: 14px;}
    .gemini-box { padding: 20px; border-radius: 10px; background-color: #e8f5e9; border: 1px solid #2e7d32; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 2. SETUP GEMINI API (Mengambil Kunci Rahasia dari Streamlit)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
except:
    st.error("⚠️ Kunci API Gemini belum dipasang di pengaturan rahasia (Secrets) Streamlit!")
    st.stop()

# 3. LOAD AI PUSTAKAWAN & DATABASE
@st.cache_resource
def load_system():
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    client = chromadb.PersistentClient(path="./agro_tanya_db")
    collection = client.get_collection(name="agro_tanya_padi_jagung")
    return model, collection

model, collection = load_system()

# 4. UI TAMPILAN
st.title("🌱 AGRO-TANYA AI")
st.write("Tanyakan keluhan hama, penyakit, atau perawatan Padi & Jagung Anda.")

query = st.text_input("Contoh: Daun jagung saya bule dan menguning, obatnya apa?")

if query:
    with st.spinner("🔍 Mencari buku pedoman Kementan..."):
        # A. FASE RETRIEVAL (Mencari Fakta)
        query_vector = model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)
        
        # Mengumpulkan teks referensi dari database
        referensi_teks = ""
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            referensi_teks += f"- [{meta.get('Judul', 'Sumber')}] {doc}\n\n"

    with st.spinner("🤖 Gemini sedang merangkum jawaban untuk Anda..."):
        # B. FASE GENERATIVE (Gemini Merangkai Kata)
        prompt = f"""
        Anda adalah asisten ahli pertanian bernama 'AGRO-TANYA'.
        Seorang petani bertanya: "{query}"
        
        TUGAS ANDA: Jawab pertanyaan tersebut HANYA berdasarkan referensi pedoman Kementan di bawah ini.
        Jangan mengarang informasi di luar referensi ini. Jika di referensi tidak ada jawabannya, bilang saja "Maaf, informasi tidak ditemukan di buku saku."
        Buat jawaban yang ramah, sopan, dan mudah dipahami petani.
        
        REFERENSI KEMENTAN:
        {referensi_teks}
        """
        
        try:
            response = gemini_model.generate_content(prompt)
            # Tampilkan Jawaban Pintar Gemini
            st.markdown(f"<div class='gemini-box'><b>👨‍🌾 Jawaban AGRO-TANYA:</b><br><br>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal memanggil Gemini: {e}")

    # C. TAMPILKAN BUKTI ASLI (Agar Dosen Yakin AI Tidak Halusinasi)
    st.subheader("📚 Fakta Asli dari Database (Ground Truth):")
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        st.markdown(f"<div class='res-box'><b>Sumber: {meta.get('Judul', '-')}</b><br>{doc}</div>", unsafe_allow_html=True)