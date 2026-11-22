"""Kerangka tampilan bersama: navbar pil, stepper, footer, dan label grade.

Hanya presentasi. Perpindahan halaman memakai ``st.session_state["langkah"]``
yang sama dengan alur sebelumnya (mulai -> identitas -> gejala -> hasil).
"""

import streamlit as st

from . import theme

# Langkah aplikasi -> tab navbar yang menyala (0 Beranda, 1 Diagnosis, 2 Dataset)
TAB_AKTIF = {"mulai": 0, "identitas": 1, "gejala": 1, "hasil": 1, "dataset": 2}
LANGKAH_ALUR = ("identitas", "gejala", "hasil")

DESKRIPSI_FOOTER = (
    "Alat bantu belajar berbasis Case-Based Reasoning. Data: RSUD dr. Soeselo "
    "Slawi (Jatmiko dkk., 2017). Bukan pengganti pemeriksaan dokter."
)

BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
    "Agustus", "September", "Oktober", "November", "Desember",
]


def romawi(kasus):
    """'Demam Berdarah Grade II' -> 'II' (cadangan: kode kasus)."""

    nama = str(kasus.get("nama", "")).split()
    if len(nama) >= 2 and nama[-2].lower() == "grade":
        return nama[-1]
    return str(kasus.get("kode", ""))


def label_grade(kasus):
    """'DHF2' / Grade II -> 'DHF-II' seperti tampilan referensi."""

    kode = str(kasus.get("kode", ""))
    if kode.upper().startswith("DHF"):
        return "DHF-" + romawi(kasus)
    return kode


def tanggal_indonesia(tgl):
    return f"{tgl.day} {BULAN[tgl.month - 1]} {tgl.year}"


def tab_aktif():
    return TAB_AKTIF.get(st.session_state.get("langkah", "mulai"), 0)


def navbar():
    """Navbar pil melayang di bagian atas."""

    langkah = st.session_state.get("langkah", "mulai")

    with st.container(key="nav"):
        kolom = st.columns(4)
        with kolom[0]:
            theme.html(
                f'<div class="brand">{theme.ikon("activity", 24)}<span class="bt">CekDBD</span></div>'
            )
        with kolom[1]:
            if st.button("Beranda", key="nav_0"):
                st.session_state["langkah"] = "mulai"
                st.rerun()
        with kolom[2]:
            if st.button("Diagnosis", key="nav_1"):
                if langkah not in LANGKAH_ALUR:
                    st.session_state["langkah"] = "identitas"
                st.rerun()
        with kolom[3]:
            if st.button("Dataset", key="nav_2"):
                st.session_state["langkah"] = "dataset"
                st.rerun()


def stepper(n):
    """Daftar langkah vertikal (Identitas, Gejala, Hasil). ``n`` = langkah aktif (1-3)."""

    nama = [
        ("Identitas", "Data pasien"),
        ("Gejala", "Pilih keluhan"),
        ("Hasil", "Kemiripan kasus"),
    ]
    item = ""
    for i, (judul, ket) in enumerate(nama, start=1):
        kelas = "done" if i < n else ("now" if i == n else "")
        titik = theme.ikon("check", 14) if i < n else str(i)
        item += (
            f'<li class="{kelas}"><span class="dt">{titik}</span>'
            f"<div><b>{judul}</b><small>{ket}</small></div></li>"
        )
    return f'<ol class="vs">{item}</ol>'


def footer():
    theme.html(
        f'<div class="foot"><b>CekDBD</b><p>{DESKRIPSI_FOOTER}</p></div>'
    )
