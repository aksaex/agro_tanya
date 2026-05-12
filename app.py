import streamlit as st
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman
st.set_page_config(page_title="AGRO-TANYA | Home", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")

# 2. Menyembunyikan Header/Footer bawaan Streamlit agar full screen
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

# 3. KODE HTML & TAILWIND (Dibungkus dalam string)
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #F9FAFB; margin: 0; padding: 0; }
        h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; }
        
        /* Animasi masuk perlahan */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fade-in { animation: fadeIn 0.8s ease-out forwards; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">
    
    <div class="relative bg-green-700 overflow-hidden shadow-xl">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center animate-fade-in">
            <span class="inline-block bg-green-900 text-green-200 text-xs font-bold px-4 py-2 rounded-full uppercase tracking-widest mb-6 border border-green-500">
                Inovasi Kecerdasan Buatan
            </span>
            <h1 class="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl mb-6">
                AGRO <span class="text-green-300">TANYA</span>
            </h1>
            <p class="mt-3 max-w-md mx-auto text-lg text-green-100 sm:text-xl md:mt-5 md:max-w-3xl">
                Sistem Temu Kembali Informasi Berbasis AI untuk Dokumen Penyuluhan Pertanian Wilayah Parepare & Ajatappareng.
            </p>
            <div class="mt-10 max-w-sm mx-auto sm:max-w-none sm:flex sm:justify-center">
                <div class="space-y-4 sm:space-y-0 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5">
                    <div class="flex items-center justify-center px-8 py-3 border border-transparent text-base font-semibold rounded-full text-green-700 bg-white shadow-lg">
                        👈 Klik Menu "Penyuluh" di Panel Kiri Layar
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="py-16 bg-white border-b border-gray-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 animate-fade-in" style="animation-delay: 0.2s;">
            <div class="text-center">
                <h2 class="text-sm text-green-600 font-bold tracking-widest uppercase">Discover Our Vision</h2>
                <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                    Mentransformasi Pertanian melalui Solusi AI
                </p>
                <p class="mt-4 max-w-3xl text-lg text-gray-500 mx-auto">
                    Kolektif mahasiswa Institut Teknologi Bacharuddin Jusuf Habibie (ITH) yang penuh semangat mentransformasi pertanian melalui inovasi Information Retrieval dan RAG. Kami menjembatani AI mutakhir dengan tantangan petani lokal.
                </p>
            </div>
        </div>
    </div>

    <div class="py-16 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center animate-fade-in" style="animation-delay: 0.4s;">
            <h2 class="text-3xl font-extrabold text-gray-900 mb-12">The Team Behind The Code</h2>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Muh+Aksa&background=10B981&color=fff&size=200" alt="Muh. Aksa">
                    <h3 class="text-lg font-bold text-gray-900">Muh. Aksa</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">Project Lead & AI Engineer</p>
                    <p class="text-xs text-gray-400 font-mono">231011101</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Aryaguna+Pasuleri&background=10B981&color=fff&size=200" alt="Aryaguna">
                    <h3 class="text-lg font-bold text-gray-900">Aryaguna Pasuleri</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">Data Engineer (Vector DB)</p>
                    <p class="text-xs text-gray-400 font-mono">231011022</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Warsila+Agimnastiar&background=10B981&color=fff&size=200" alt="Warsila">
                    <h3 class="text-lg font-bold text-gray-900">Warsila Agimnastiar</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">Frontend & UI/UX</p>
                    <p class="text-xs text-gray-400 font-mono">231011116</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Safri+Nur+Saputra&background=10B981&color=fff&size=200" alt="Safri">
                    <h3 class="text-lg font-bold text-gray-900">Safri Nur Saputra</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">Data Analyst (Corpus)</p>
                    <p class="text-xs text-gray-400 font-mono">231011086</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Sitti+Fatima&background=10B981&color=fff&size=200" alt="Sitti Fatima">
                    <h3 class="text-lg font-bold text-gray-900">Sitti Fatima</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">Prompt & QA Engineer</p>
                    <p class="text-xs text-gray-400 font-mono">231011092</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 transform transition duration-300 hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-28 h-28 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-50" src="https://ui-avatars.com/api/?name=Jumrianti&background=10B981&color=fff&size=200" alt="Jumrianti">
                    <h3 class="text-lg font-bold text-gray-900">Jumrianti</h3>
                    <p class="text-green-600 font-medium text-sm mb-1">IR Evaluation Researcher</p>
                    <p class="text-xs text-gray-400 font-mono">231011007</p>
                </div>
            </div>
        </div>
    </div>

    <div class="bg-gray-900 py-10 text-center">
        <p class="text-gray-400 text-sm">© 2026 Proyek IR AGRO-TANYA | Institut Teknologi Bacharuddin Jusuf Habibie.</p>
    </div>

</body>
</html>
"""

# 4. MENGINJEKSI HTML KE DALAM IFRAME STREAMLIT (Tinggi di-set panjang agar bisa di-scroll)
components.html(html_code, height=1900, scrolling=True)