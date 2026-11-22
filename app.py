"""Aplikasi Streamlit - CekDBD sederhana untuk pengguna umum.

Alur: data diri -> pilih gejala -> hasil.
Jalankan dengan:

    streamlit run app.py

Tampilan mengikuti aplikasi referensi (HTML/CSS/JS); logika diagnosis tetap
berada di ``core/`` dan tidak diubah.
"""

import streamlit as st

from components import dashboard, info_view, input_form, layout, result_view, theme
from data.dataset import DHF


st.set_page_config(
    page_title="CekDBD - Cek Grade Demam Berdarah",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "langkah" not in st.session_state:
    st.session_state["langkah"] = "mulai"

theme.terapkan([atribut["kode"] for atribut in DHF.atribut], layout.tab_aktif())

input_form.init_state(DHF)

layout.navbar()

langkah = st.session_state["langkah"]

if langkah == "mulai":
    dashboard.render(DHF)
    info_view.render_tentang_ringkas()
elif langkah == "identitas":
    input_form.render_identitas()
elif langkah == "gejala":
    input_form.render_gejala(DHF)
elif langkah == "hasil":
    result_view.render_hasil(st.session_state.get("hasil"), DHF)
elif langkah == "dataset":
    info_view.render_dataset(DHF)

layout.footer()

# Setiap berpindah langkah (mis. "Lihat hasil"), halaman dikembalikan ke atas
# agar pengguna langsung melihat isi halaman baru, bukan posisi gulir sebelumnya.
if st.session_state.get("_langkah_tampil") != langkah:
    st.session_state["_langkah_tampil"] = langkah
    theme.gulir_ke_atas()