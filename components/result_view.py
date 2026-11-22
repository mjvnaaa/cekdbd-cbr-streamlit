"""Tampilan hasil yang mudah dipahami pengguna umum."""

import datetime

import streamlit as st

from core.basis_kasus import retain
from core.cbr import revise
from . import layout, theme


def tabel_markdown(headers, rows):
    """Membuat tabel Markdown tanpa bantuan Pandas."""

    def sel(value):
        return str(value).replace("|", "\\|")

    baris_header = "| " + " | ".join(sel(h) for h in headers) + " |"
    baris_pemisah = "| " + " | ".join("---" for _ in headers) + " |"
    baris_data = "\n".join(
        "| " + " | ".join(sel(value) for value in row) + " |" for row in rows
    )
    return "\n".join([baris_header, baris_pemisah, baris_data])


def _kosong():
    theme.html('<div class="page-top"></div>')
    with st.container(key="card_kosong"):
        theme.html(
            """
            <div class="card-h"><h2>Hasil Pemeriksaan</h2>
            <p>Belum ada hasil pemeriksaan. Isi data diri dan pilih gejala terlebih dahulu.</p></div>
            """
        )
        if st.button(
            "Mulai pemeriksaan",
            key="btn_mulai_kosong",
            type="primary",
            icon=":material/arrow_forward:",
        ):
            st.session_state["langkah"] = "identitas"
            st.rerun()


def _lembar_laporan(state, dataset, pasien):
    """HTML lembar laporan (angka berasal dari ``state`` hasil core/cbr.py)."""

    terbaik = state["terbaik"]
    daftar = state["hasil"]
    kasusbaru = state["kasusbaru"]
    cocok = terbaik["cosine"] > 0

    kasus_per_kode = {k["kode"]: k for k in dataset.kasus_lama}

    # Basis kasus dapat berisi kasus hasil Retain. Grafik menampilkan satu
    # batang per grade rujukan: kemiripan tertinggi di antara kasus bergrade itu.
    terbaik_per_grade = {}
    for item in daftar:
        sebelumnya = terbaik_per_grade.get(item["nama"])
        if sebelumnya is None or item["cosine"] > sebelumnya["cosine"]:
            terbaik_per_grade[item["nama"]] = item

    skala = ""
    kolom = ""
    for kasus in dataset.kasus_lama:
        item = terbaik_per_grade.get(kasus["nama"])
        if item is None:
            continue
        puncak = cocok and kasus["nama"] == terbaik["nama"]
        kelas = "on" if puncak else ""
        skala += f'<div class="{kelas}">{theme.esc(layout.romawi(kasus))}</div>'
        tinggi = max(0.0, min(1.0, item["cosine"])) * 120
        kolom += (
            f'<div class="col {"top" if puncak else ""}"><div class="area">'
            f'<span class="v">{item["persentase"]:.1f}%</span>'
            f'<div class="b" style="--h:{tinggi:.0f}px"></div></div>'
            f"<small>{theme.esc(layout.label_grade(kasus))}</small></div>"
        )

    tag = "".join(
        f'<span class="tag">{theme.esc(a["nama"])}</span>'
        for a, nilai in zip(dataset.atribut, kasusbaru)
        if nilai == 1
    )
    jumlah_gejala = sum(1 for nilai in kasusbaru if nilai == 1)

    if cocok:
        kasus_t = kasus_per_kode.get(terbaik["kode"], terbaik)
        utama = (
            f'<div><p class="lbl">Kasus paling mirip</p>'
            f'<div class="big">{theme.esc(layout.label_grade(kasus_t))}</div>'
            f'<p class="grade-name">{theme.esc(terbaik["nama"])}</p>'
            f'<div class="scale">{skala}</div></div>'
            f'<div><p class="lbl">Tingkat kemiripan</p>'
            f'<div class="pct">{terbaik["persentase"]:.1f}%</div>'
            f'<p class="pct-note">dengan kasus {theme.esc(terbaik["kode"])}'
            f' (dari {state.get("jumlah_basis", len(daftar))} kasus dalam basis)</p></div>'
        )
    else:
        utama = (
            '<div><p class="lbl">Hasil</p>'
            '<div class="big sm">Belum ada grade yang cocok</div>'
            '<p class="nomatch">Gejala ini tidak menyerupai kasus DHF mana pun. '
            "Periksakan ke dokter bila keluhan berlanjut.</p></div>"
        )

    tanggal = layout.tanggal_indonesia(datetime.date.today())

    return f"""
    <article class="sheet">
      <div class="sh-top"><b>{theme.ikon("file-text", 16)} Laporan pemeriksaan</b><span>{tanggal}</span></div>
      <div class="sh-main">{utama}</div>
      <div class="sh-body">
        <div class="blk"><h3>Data pasien</h3><dl>
          <dt>Nama</dt><dd>{theme.esc(pasien.get("nama", "-"))}</dd>
          <dt>Usia</dt><dd>{theme.esc(pasien.get("usia", "-"))} tahun</dd>
          <dt>Jenis kelamin</dt><dd>{theme.esc(pasien.get("jk", "-"))}</dd></dl></div>
        <div class="blk"><h3>Gejala yang dipilih ({jumlah_gejala})</h3>{tag}</div>
      </div>
      <div class="blk top"><h3>Perbandingan dengan tiap grade</h3><div class="chart">{kolom}</div></div>
    </article>
    <div class="note">{theme.ikon("info", 18)}<span>Nilai kemiripan menunjukkan seberapa dekat gejala
    pasien dengan kasus rujukan, bukan peluang pasti diagnosis. Hasil ini rekomendasi awal dan perlu
    dikonfirmasi dokter.</span></div>
    """


def _kartu_revisi_retain(state, dataset):
    """Tahap Revise (tinjau solusi) dan Retain (simpan ke basis kasus)."""

    usulan = state.get("usulan")
    if not usulan:
        return

    hasil_retain = state.get("retain")
    revisi = state.get("revisi")

    with st.container(key="card_revisi"):
        if usulan["grade"]:
            teks_usulan = (
                f'Usulan sistem (Reuse): <b>{theme.esc(usulan["grade"])}</b>, '
                f'diambil dari kasus {theme.esc(usulan["kode_kasus"])}.'
            )
        else:
            teks_usulan = (
                "Sistem tidak menemukan kasus yang mirip, jadi belum ada usulan grade."
            )
        theme.html(
            f"""
            <div class="card-h"><h2>Tinjau dan simpan kasus</h2>
            <p>{teks_usulan} Periksa apakah grade ini sudah tepat (Revise), lalu simpan
            kasus ke basis kasus agar dipakai pada pemeriksaan berikutnya (Retain).
            Yang disimpan hanya pola gejala dan grade, bukan identitas pasien.</p></div>
            """
        )

        if hasil_retain:
            kasus = hasil_retain["kasus"]
            if revisi and revisi["direvisi"]:
                asal = (
                    f'direvisi dari {theme.esc(revisi["grade_usulan"])}'
                    if revisi["grade_usulan"]
                    else "ditentukan manual"
                )
            else:
                asal = "sesuai usulan sistem"
            theme.html(
                f'<div class="note flat"><span>Solusi akhir: '
                f'<b>{theme.esc(kasus["nama"])}</b> ({asal}).</span></div>'
            )
            if hasil_retain["status"] == "disimpan":
                st.success(
                    f"Kasus disimpan sebagai {kasus['kode']}. "
                    "Kasus ini ikut dibandingkan pada pemeriksaan berikutnya."
                )
            else:
                st.info(
                    f"Pola gejala yang sama dengan grade ini sudah ada di basis kasus "
                    f"({kasus['kode']}), jadi tidak disimpan ulang."
                )
            return

        if usulan["perlu_ditinjau"]:
            st.warning(
                "Kemiripan rendah, hasil seri, atau tidak ada yang cocok. "
                "Tinjau grade dengan teliti sebelum menyimpan."
            )

        opsi = list(dataset.nama_kasus)
        indeks = opsi.index(usulan["grade"]) if usulan["grade"] in opsi else None
        st.selectbox(
            "Grade akhir",
            options=opsi,
            index=indeks,
            key="revisi_grade",
            placeholder="Pilih grade",
        )
        st.text_input(
            "Catatan peninjau (opsional)",
            key="revisi_catatan",
            placeholder="Contoh: dikonfirmasi dokter",
        )
        ruang_galat = st.empty()
        simpan = st.button(
            "Simpan ke basis kasus",
            key="btn_simpan_kasus",
            type="primary",
            icon=":material/save:",
        )

        if simpan:
            try:
                solusi = revise(
                    usulan,
                    st.session_state.get("revisi_grade"),
                    opsi,
                    st.session_state.get("revisi_catatan", ""),
                )
                state["retain"] = retain(dataset, state["kasusbaru"], solusi)
                state["revisi"] = solusi
                st.rerun()
            except ValueError as error:
                with ruang_galat:
                    theme.galat(str(error))


def render_hasil(state, dataset):
    if not state:
        _kosong()
        return

    pasien = st.session_state.get("pasien") or {}

    theme.html('<div class="page-top"></div>')
    with st.container(key="wrap920"):
        theme.html(_lembar_laporan(state, dataset, pasien))
        _kartu_revisi_retain(state, dataset)

        with st.container(key="acts"):
            if st.button(
                "Ubah gejala",
                key="btn_ubah_gejala",
                icon=":material/arrow_back:",
            ):
                st.session_state["langkah"] = "gejala"
                st.rerun()
            if st.button(
                "Periksa pasien lain",
                key="btn_periksa_lain",
                type="primary",
                icon=":material/restart_alt:",
            ):
                from .input_form import reset_state

                reset_state(dataset)
                st.rerun()
