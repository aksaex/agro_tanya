import streamlit as st

# Konfigurasi Halaman Wajib (Harus paling atas)
st.set_page_config(page_title="AGRO-TANYA | Home", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------
# INJEKSI TAILWIND CSS VIA CDN & HTML MURNI
# ---------------------------------------------------------
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<style>
    /* Menyembunyikan elemen bawaan Streamlit agar terasa seperti web asli */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
</style>

<div class="bg-gray-50 min-h-screen font-sans text-gray-800">
    
    <div class="relative bg-green-700 overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
            <h1 class="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl mb-6">
                AGRO <span class="text-green-300">TANYA</span>
            </h1>
            <p class="mt-3 max-w-md mx-auto text-lg text-green-100 sm:text-xl md:mt-5 md:max-w-3xl">
                Sistem Temu Kembali Informasi Berbasis AI untuk Dokumen Penyuluhan Pertanian Wilayah Parepare & Ajatappareng.
            </p>
            <div class="mt-10 max-w-sm mx-auto sm:max-w-none sm:flex sm:justify-center">
                <div class="space-y-4 sm:space-y-0 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5">
                    <a href="#" class="flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-green-700 bg-white hover:bg-green-50 md:py-4 md:text-lg transition shadow-lg">
                        👈 Buka Menu Chatbot di Kiri
                    </a>
                </div>
            </div>
        </div>
    </div>

    <div class="py-16 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <h2 class="text-base text-green-600 font-semibold tracking-wide uppercase">Discover Our Vision</h2>
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
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-3xl font-extrabold text-gray-900 mb-12">The Team Behind The Code</h2>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">
                
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Muh+Aksa&background=10B981&color=fff&size=200" alt="Muh. Aksa">
                    <h3 class="text-xl font-bold text-gray-900">Muh. Aksa</h3>
                    <p class="text-green-600 font-medium mb-2">Project Lead & AI Engineer</p>
                    <p class="text-sm text-gray-500">231011101</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Aryaguna+Pasuleri&background=10B981&color=fff&size=200" alt="Aryaguna">
                    <h3 class="text-xl font-bold text-gray-900">Aryaguna Pasuleri</h3>
                    <p class="text-green-600 font-medium mb-2">Data Engineer (Vector DB)</p>
                    <p class="text-sm text-gray-500">231011022</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Warsila+Agimnastiar&background=10B981&color=fff&size=200" alt="Warsila">
                    <h3 class="text-xl font-bold text-gray-900">Warsila Agimnastiar</h3>
                    <p class="text-green-600 font-medium mb-2">Frontend & UI/UX</p>
                    <p class="text-sm text-gray-500">231011116</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Safri+Nur+Saputra&background=10B981&color=fff&size=200" alt="Safri">
                    <h3 class="text-xl font-bold text-gray-900">Safri Nur Saputra</h3>
                    <p class="text-green-600 font-medium mb-2">Data Analyst (Corpus)</p>
                    <p class="text-sm text-gray-500">231011086</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Sitti+Fatima&background=10B981&color=fff&size=200" alt="Sitti Fatima">
                    <h3 class="text-xl font-bold text-gray-900">Sitti Fatima</h3>
                    <p class="text-green-600 font-medium mb-2">Prompt & QA Engineer</p>
                    <p class="text-sm text-gray-500">231011092</p>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 transform transition hover:-translate-y-2 hover:shadow-xl">
                    <img class="w-32 h-32 mx-auto rounded-full object-cover mb-4 ring-4 ring-green-100" src="https://ui-avatars.com/api/?name=Jumrianti&background=10B981&color=fff&size=200" alt="Jumrianti">
                    <h3 class="text-xl font-bold text-gray-900">Jumrianti</h3>
                    <p class="text-green-600 font-medium mb-2">IR Evaluation Researcher</p>
                    <p class="text-sm text-gray-500">231011007</p>
                </div>

            </div>
        </div>
    </div>

    <div class="bg-gray-900 py-8 text-center">
        <p class="text-gray-400 text-sm">© 2026 Proyek IR AGRO-TANYA | Institut Teknologi Bacharuddin Jusuf Habibie.</p>
    </div>

</div>
""", unsafe_allow_html=True)