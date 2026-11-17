"""Tampilan hasil yang mudah dipahami pengguna umum."""

import datetime

import streamlit as st

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
            <div style="height:18px"></div>
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
    theme.html('<div class="page-bot"></div>')


def _lembar_laporan(state, dataset, pasien):
    """HTML lembar laporan (angka berasal dari ``state`` hasil core/cbr.py)."""

    terbaik = state["terbaik"]
    daftar = state["hasil"]
    kasusbaru = state["kasusbaru"]
    cocok = terbaik["cosine"] > 0

    kasus_per_kode = {k["kode"]: k for k in dataset.kasus_lama}

    skala = ""
    kolom = ""
    for item in daftar:
        kasus = kasus_per_kode.get(item["kode"], item)
        puncak = cocok and item["kode"] == terbaik["kode"]
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
            f'<p style="margin-top:8px;font-weight:600;color:var(--deep-twilight)">{theme.esc(terbaik["nama"])}</p>'
            f'<div class="scale">{skala}</div></div>'
            f'<div><p class="lbl">Tingkat kemiripan</p>'
            f'<div class="pct">{terbaik["persentase"]:.1f}%</div>'
            f'<p class="mute" style="font-size:.85rem">dengan kasus {theme.esc(terbaik["kode"])}</p></div>'
        )
    else:
        utama = (
            '<div><p class="lbl">Hasil</p>'
            '<div class="big" style="font-size:clamp(1.8rem,6vw,2.6rem)">Belum ada grade yang cocok</div>'
            '<p class="mute" style="margin-top:10px">Gejala ini tidak menyerupai kasus DHF mana pun. '
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


def render_hasil(state, dataset):
    if not state:
        _kosong()
        return

    pasien = st.session_state.get("pasien") or {}

    theme.html('<div class="page-top"></div>')
    with st.container(key="wrap920"):
        theme.html(_lembar_laporan(state, dataset, pasien))

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
    theme.html('<div class="page-bot"></div>')
