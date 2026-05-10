import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AGRO-TANYA", page_icon="🌱", layout="centered")

# Custom CSS agar tampilan lebih keren
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; }
    .res-box { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #2e7d32; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOAD AI & DATABASE (Caching agar cepat)
@st.cache_resource
def load_system():
    # Load Model Pustakawan
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    # Load Database Rak Buku
    client = chromadb.PersistentClient(path="./agro_tanya_db")
    collection = client.get_collection(name="agro_tanya_padi_jagung")
    return model, collection

model, collection = load_system()

# 3. UI - HEADER
st.title("🌱 AGRO-TANYA")
st.subheader("Sistem Pakar Pertanian Ajatappareng")
st.write("Tanyakan keluhan hama, penyakit, atau perawatan Padi & Jagung Anda.")

# 4. FITUR PENCARIAN
query = st.text_input("Contoh: Daun jagung saya ada bercak putih, obatnya apa?", placeholder="Ketik di sini...")

if query:
    with st.spinner("Sedang mencari jawaban di database Kementan..."):
        # Ubah pertanyaan jadi angka (Embedding)
        query_vector = model.encode(query).tolist()
        
        # Cari di ChromaDB (Ambil 3 hasil paling relevan)
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=3
        )
        
        # TAMPILKAN HASIL
        st.success(f"Ditemukan {len(results['documents'][0])} informasi yang relevan:")
        
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            
            with st.container():
                st.markdown(f"""
                <div class="res-box">
                    <b>📄 Sumber: {meta.get('Judul', 'Dokumen Pertanian')}</b><br>
                    <small>🏷️ Komoditas: {meta.get('Komoditas', '-')} | Kategori: {meta.get('Kategori', '-')}</small><br><br>
                    {doc}
                </div>
                """, unsafe_allow_html=True)

# 5. SIDEBAR INFO
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2510/2510168.png", width=100)
    st.title("Tentang Proyek")
    st.info("Sistem ini menggunakan arsitektur RAG (Retrieval-Augmented Generation) untuk memberikan jawaban anti-halusinasi bagi petani.")
    st.write(" Tim 6 Orang - Mata Kuliah IR")