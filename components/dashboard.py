"""Halaman Beranda (hero, cara kerja, penjelasan metode)."""

import streamlit as st

from . import layout, theme


def render(dataset):
    # ----- hero -----
    with st.container(key="hero"):
        kiri, kanan = st.columns([1.15, 0.85])
        with kiri:
            theme.html(
                f"""
                <span class="pill">{theme.ikon("shield-check", 16)} Case-Based Reasoning</span>
                <h1>Gejala yang kamu rasakan, dicocokkan dengan kasus nyata.</h1>
                <p class="lead">Sistem membandingkan gejala pasien dengan {dataset.jumlah_kasus}
                kasus rujukan dari rekam medis RSUD dr. Soeselo Slawi, lalu menunjukkan
                grade demam berdarah yang paling mirip.</p>
                """
            )
            with st.container(key="cta"):
                if st.button(
                    "Mulai Pemeriksaan",
                    key="hero_start",
                    icon=":material/arrow_forward:",
                ):
                    st.session_state["langkah"] = "identitas"
                    st.rerun()
                if st.button("Lihat dataset", key="hero_data"):
                    st.session_state["langkah"] = "dataset"
                    st.rerun()
        with kanan:
            kipas = "".join(
                f"<div><b>{layout.romawi(k)}</b><small>Grade</small></div>"
                for k in dataset.kasus_lama
            )
            theme.html(f'<div class="fan" aria-hidden="true">{kipas}</div>')

    # ----- cara kerjanya -----
    info = [
        ("user-round", "Langkah 1", "Isi identitas",
         "Catat nama, usia, dan jenis kelamin pasien untuk laporan pemeriksaan."),
        ("clipboard-list", "Langkah 2", "Pilih gejala",
         "Centang keluhan dan kelainan hasil lab darah yang dialami pasien."),
        ("file-text", "Langkah 3", "Baca hasil",
         "Lihat grade DHF yang paling mirip beserta tingkat kemiripannya."),
    ]
    kartu = "".join(
        f'<div class="st-card"><div class="stt"><small>{langkah}</small>{theme.ikon(nama_ikon, 26)}</div>'
        f"<h3>{judul}</h3><p>{isi}</p></div>"
        for nama_ikon, langkah, judul, isi in info
    )
    theme.html(
        f"""
        <section class="blok"><h2>Cara kerjanya</h2>
        <p class="sec-sub">Tiga langkah, tanpa perlu memahami perhitungannya.</p>
        <div class="g3">{kartu}</div></section>
        """
    )

    # ----- metode -----
    contoh = dataset.kasus_lama[1] if len(dataset.kasus_lama) > 1 else dataset.kasus_lama[0]
    bit = "".join(
        f'<i class="{"on" if contoh["vektor"][j] == 1 else ""}" title="{theme.esc(a["nama"])}"></i>'
        for j, a in enumerate(dataset.atribut)
    )
    theme.html(
        f"""
        <section class="blok"><div class="metode">
        <div><h2>Gejala diubah menjadi pola</h2>
        <p>Setiap gejala bernilai 1 bila ada dan 0 bila tidak.
        Pola pasien dibandingkan dengan pola tiap kasus rujukan memakai Cosine Similarity.
        Nilainya menunjukkan kemiripan kasus, bukan peluang pasti diagnosis.</p></div>
        <div><div class="bits" style="grid-template-columns:repeat({dataset.jumlah_atribut},1fr)">{bit}</div>
        <p class="bits-cap">Contoh pola gejala kasus
        {theme.esc(layout.label_grade(contoh))}. Kotak terang berarti gejala ada.</p></div>
        </div></section>
        """
    )
