"""Alur input sederhana untuk pengguna umum.

Langkah: data diri -> pilih gejala -> hasil.
Identitas hanya dipakai untuk menampilkan laporan, bukan untuk perhitungan.
"""

import streamlit as st

from core.basis_kasus import muat_basis
from core.cbr import (
    buat_kasus_baru,
    hitung_cbr,
    kasus_terbaik,
    reuse,
    urutkan_hasil,
)
from . import layout, theme
from utils.validation import (
    validasi_pasien,
    validasi_pilihan_gejala,
    validasi_vektor,
)


# Kunci widget tahap Revise; dibersihkan setiap kali ada hasil baru.
KUNCI_REVISI = ["revisi_grade", "revisi_catatan"]


def _kunci_gejala(kode):
    return f"gejala_{kode}"


def init_state(dataset):
    """Menyiapkan nilai awal form."""

    st.session_state.setdefault("nama", "")
    st.session_state.setdefault("usia", 0)
    st.session_state.setdefault("jk", None)
    st.session_state.setdefault("pasien", None)
    st.session_state.setdefault("pilih", [])
    st.session_state.setdefault("hasil", None)

    for atribut in dataset.atribut:
        st.session_state.setdefault(_kunci_gejala(atribut["kode"]), False)

    # Streamlit membuang state widget yang tidak tampil pada satu putaran. Menugaskan
    # ulang nilainya menjaga isian tetap ada saat pengguna berpindah halaman
    # (mis. kembali dari hasil ke pilihan gejala), seperti sessionStorage di referensi.
    kunci = ["nama", "usia", "jk"] + [_kunci_gejala(a["kode"]) for a in dataset.atribut]
    for k in kunci:
        st.session_state[k] = st.session_state[k]


def reset_state(dataset):
    """Mengosongkan seluruh input dan kembali ke halaman awal."""

    for kunci in ["nama", "usia", "jk", "pasien", "pilih", "hasil"] + KUNCI_REVISI:
        st.session_state.pop(kunci, None)

    for atribut in dataset.atribut:
        st.session_state.pop(_kunci_gejala(atribut["kode"]), None)

    st.session_state["langkah"] = "mulai"


def kumpulkan_gejala(dataset):
    """Mengubah centangan gejala menjadi daftar kode."""

    return [
        atribut["kode"]
        for atribut in dataset.atribut
        if st.session_state.get(_kunci_gejala(atribut["kode"]), False)
    ]


def _simpan_hasil(dataset, pilih):
    """Menjalankan Retrieve + Reuse dan menyimpan hasilnya di session state."""

    # Retrieve membandingkan kasus baru dengan seluruh basis kasus:
    # kasus rujukan awal + kasus yang pernah disimpan lewat Retain.
    basis = muat_basis(dataset)
    kasusbaru = buat_kasus_baru(pilih, dataset.atribut)
    validasi_vektor(kasusbaru, basis, dataset.jumlah_atribut)

    hasil = hitung_cbr(kasusbaru, basis)

    for kunci in KUNCI_REVISI:
        st.session_state.pop(kunci, None)

    st.session_state["pilih"] = pilih
    st.session_state["hasil"] = {
        "kasusbaru": kasusbaru,
        "hasil": hasil,
        "ranking": urutkan_hasil(hasil),
        "terbaik": kasus_terbaik(hasil),
        "usulan": reuse(hasil),
        "jumlah_basis": len(basis),
        "revisi": None,
        "retain": None,
    }
    st.session_state["langkah"] = "hasil"
    st.rerun()


def render_identitas():
    theme.html('<div class="page-top"></div>')
    with st.container(key="split_ident"):
        sisi, utama = st.columns([1, 2.3])

        with sisi:
            with st.container(key="card_side"):
                theme.html(
                    '<div class="side-h"><h3>Alur pemeriksaan</h3></div>' + layout.stepper(1)
                )

        with utama:
            with st.container(key="card_main"):
                theme.html(
                    """
                    <div class="card-h"><h2>Data pasien</h2>
                    <p>Identitas hanya untuk melengkapi laporan dan tidak ikut dihitung.</p></div>
                    """
                )
                with st.form("form_identitas", clear_on_submit=False):
                    st.text_input(
                        "Nama lengkap",
                        key="nama",
                        placeholder="Contoh: Azhar",
                    )
                    kol_usia, kol_jk = st.columns(2)
                    with kol_usia:
                        st.number_input(
                            "Usia (tahun)",
                            min_value=0,
                            max_value=120,
                            key="usia",
                        )
                    with kol_jk:
                        st.radio(
                            "Jenis kelamin",
                            options=["Laki-laki", "Perempuan"],
                            key="jk",
                            index=None,
                            horizontal=True,
                        )
                    ruang_galat = st.empty()
                    lanjut = st.form_submit_button(
                        "Lanjut pilih gejala",
                        type="primary",
                        icon=":material/arrow_forward:",
                    )

                if lanjut:
                    try:
                        st.session_state["pasien"] = validasi_pasien(
                            st.session_state["nama"],
                            st.session_state["usia"],
                            st.session_state["jk"],
                        )
                        st.session_state["langkah"] = "gejala"
                        st.rerun()
                    except ValueError as error:
                        with ruang_galat:
                            theme.galat(str(error))


def render_gejala(dataset):
    pasien = st.session_state.get("pasien")
    if not pasien:
        st.session_state["langkah"] = "identitas"
        st.rerun()
        return

    keluhan = [item for item in dataset.atribut if item["kode"] in {f"G{i}" for i in range(1, 12)}]
    laboratorium = [item for item in dataset.atribut if item["kode"] in {f"G{i}" for i in range(12, 15)}]

    theme.html('<div class="page-top"></div>')
    with st.container(key="split_gejala"):
        utama, sisi = st.columns([2.3, 1])

        with utama:
            with st.container(key="card_main"):
                theme.html(
                    f"""
                    <div class="card-h"><h2>Apa yang dirasakan {theme.esc(pasien['nama'])}?</h2>
                    <p>Ketuk kartu untuk memilih gejala. Boleh lebih dari satu.</p></div>
                    <h3 class="gh">Keluhan</h3>
                    """
                )
                with st.container(key="tiles_keluhan"):
                    for atribut in keluhan:
                        st.checkbox(atribut["nama"], key=_kunci_gejala(atribut["kode"]))

                theme.html(
                    """
                    <h3 class="gh">Hasil lab darah
                    <span class="mute">(pilih bila ada kelainan)</span></h3>
                    """
                )
                with st.container(key="tiles_lab"):
                    for atribut in laboratorium:
                        st.checkbox(atribut["nama"], key=_kunci_gejala(atribut["kode"]))

        with sisi:
            with st.container(key="card_side"):
                jumlah = len(kumpulkan_gejala(dataset))
                total = dataset.jumlah_atribut
                theme.html(
                    f"""
                    <div class="side-h"><h3>Alur pemeriksaan</h3></div>{layout.stepper(2)}
                    <div class="meter"><div class="mn"><b>{jumlah}</b><span>/ {total}<em> gejala</em></span></div>
                    <div class="prog"><i style="width:{jumlah / total * 100:.1f}%"></i></div></div>
                    """
                )
                with st.container(key="side_actions"):
                    selesai = st.button(
                        "Lihat hasil",
                        key="btn_lihat_hasil",
                        type="primary",
                        icon=":material/arrow_forward:",
                    )
                    kembali = st.button(
                        "Kembali",
                        key="btn_kembali_identitas",
                        icon=":material/arrow_back:",
                    )
                ruang_galat = st.empty()


    if kembali:
        st.session_state["langkah"] = "identitas"
        st.rerun()

    if selesai:
        try:
            pilih = kumpulkan_gejala(dataset)
            validasi_pilihan_gejala(pilih, dataset.atribut)
            _simpan_hasil(dataset, pilih)
        except ValueError as error:
            with ruang_galat:
                theme.galat(str(error))
