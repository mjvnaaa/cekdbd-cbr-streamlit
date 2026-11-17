"""Informasi akademik dan referensi (ditampilkan ringkas di halaman awal)."""

import streamlit as st

from . import layout, theme
from .result_view import tabel_markdown

JUDUL_APLIKASI = (
    "CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus "
    "Menggunakan CBR dan Cosine Similarity"
)

IDENTITAS = [
    ["Nama", "Moh. Jevon Attaillah"],
    ["NIM", "362458302035"],
    ["Kelas", "TRPL 3D"],
    ["Program studi", "Rekayasa Perangkat Lunak"],
    ["Mata kuliah", "Sistem Pendukung Keputusan (SPK)"],
    ["Judul aplikasi", JUDUL_APLIKASI],
]

REFERENSI_BIBTEX = r"""@article{Jatmiko2017,
  author    = {Jatmiko, Arman Dwi and Junaedi, Danang and Imrona, Mahmud},
  title     = {Analisis Dan Implementasi Sistem Pakar Dengan Metode Case Based Reasoning Dan Rule Based Reasoning (Studi Kasus: Diagnosis Penyakit Demam Berdarah)},
  journal   = {e-Proceeding of Engineering},
  year      = {2017},
  month     = aug,
  volume    = {4},
  number    = {2},
  pages     = {3269--3276},
  issn      = {2355-9365},
  publisher = {Universitas Telkom},
  keywords  = {case based reasoning, rule based reasoning, bayes, sistem pakar, demam berdarah},
  abstract  = {Penyakit demam berdarah merupakan salah satu penyakit menular yang sering menimbulkan wabah dan menyebabkan kematian. Pada penelitian ini dibangun sistem pakar menggunakan metode Case Based Reasoning (CBR) dan Rule Based Reasoning (RBR). Pencocokan kasus menggunakan konsep similarity dan solusi terbaik diambil berdasarkan perhitungan probabilitas bayes. Aplikasi sistem pakar untuk diagnosis demam berdarah ini mencapai tingkat akurasi sebesar 92\%.}
}"""


def render_tentang_ringkas():
    """Expander ringkas di halaman awal: identitas + referensi lengkap."""

    theme.html('<div style="height:12px"></div>')
    with st.expander("Identitas aplikasi & referensi"):
        st.markdown(tabel_markdown(["Informasi", "Keterangan"], IDENTITAS), unsafe_allow_html=True)

        st.markdown("#### Referensi")
        st.code(REFERENSI_BIBTEX, language="text")
        st.caption(
            "Referensi tersebut menjadi dasar dataset DHF. Angka akurasi 92% "
            "merupakan hasil penelitian Jatmiko dkk. (2017), bukan hasil "
            "perhitungan aplikasi ini."
        )


def render_dataset(dataset):
    """Halaman Dataset: matriks gejala x kasus rujukan (tampilan referensi, hanya baca)."""

    theme.html(
        f"""
        <div class="page-top"></div>
        <h1 class="jd">Dataset kasus rujukan</h1>
        <p class="mute" style="margin-top:8px;max-width:40em">{dataset.jumlah_kasus} kasus lama sebagai
        pembanding. Titik terisi berarti gejala ada pada grade tersebut.</p>
        """
    )

    with st.container(key="cari"):
        kata = st.text_input(
            "Cari gejala",
            key="cari_gejala",
            placeholder="Cari gejala...",
            label_visibility="collapsed",
        )

    q = (kata or "").strip().lower()
    kepala = "".join(
        f"<th>{theme.esc(layout.romawi(k))}</th>" for k in dataset.kasus_lama
    )
    baris = ""
    for index, atribut in enumerate(dataset.atribut):
        if q and q not in f"{atribut['nama']} {atribut['kode']}".lower():
            continue
        baris += f"<tr><td><b>{theme.esc(atribut['kode'])}</b> &nbsp;{theme.esc(atribut['nama'])}</td>"
        for kasus in dataset.kasus_lama:
            ada = kasus["vektor"][index] == 1
            baris += (
                f'<td><span class="dot {"y" if ada else "n"}" role="img" '
                f'aria-label="{"ada" if ada else "tidak ada"}"></span></td>'
            )
        baris += "</tr>"
    if not baris:
        baris = (
            f'<tr><td colspan="{dataset.jumlah_kasus + 1}" class="kosong">'
            "Gejala tidak ditemukan.</td></tr>"
        )

    total = "".join(
        f"<td><b>{sum(kasus['vektor'])}</b></td>" for kasus in dataset.kasus_lama
    )

    theme.html(
        f"""
        <div class="card" style="background:#fff;border:1.5px solid var(--line);border-radius:28px;padding:8px">
        <div class="scroll"><table class="tbl mat"><thead><tr><th>Gejala</th>{kepala}</tr></thead>
        <tbody>{baris}</tbody>
        <tfoot><tr><td>Jumlah gejala</td>{total}</tr></tfoot></table></div></div>
        <p class="mute" style="margin-top:14px;font-size:.88rem">Sumber: Jatmiko, Junaedi, dan Imrona (2017),
        Tabel 2-1 sampai 2-3.</p>
        <div class="page-bot"></div>
        """
    )


def render_tentang():
    """Halaman Tentang lengkap (arsip, tidak dipakai di alur pengguna umum)."""

    st.header("Tentang Aplikasi")
    st.markdown("### Identitas akademik")
    st.markdown(
        tabel_markdown(["Informasi", "Keterangan"], IDENTITAS),
        unsafe_allow_html=True,
    )

    st.markdown("### Landasan metode")
    st.markdown(
        "Case-Based Reasoning (CBR) menyelesaikan masalah baru dengan mencari "
        "kasus lama yang paling mirip. Kemiripan dihitung memakai Cosine "
        "Similarity, yaitu dot product dua vektor dibagi hasil kali panjangnya. "
        "Seluruh angka dihitung oleh kode Python di folder `core/`, bukan oleh "
        "JavaScript."
    )

    st.markdown("### Referensi")
    st.markdown(
        "Jatmiko, A. D., Junaedi, D., & Imrona, M. (2017). Analisis dan "
        "implementasi sistem pakar dengan metode Case Based Reasoning dan Rule "
        "Based Reasoning (Studi kasus: Diagnosis penyakit demam berdarah). "
        "*e-Proceeding of Engineering, 4*(2), 3269–3276. Universitas Telkom."
    )
    st.code(REFERENSI_BIBTEX, language="text")
    st.caption(
        "Referensi tersebut menjadi dasar dataset DHF. Angka akurasi 92% "
        "merupakan hasil penelitian Jatmiko dkk. (2017), bukan hasil "
        "perhitungan aplikasi ini."
    )
