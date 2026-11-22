"""Basis kasus dan tahap RETAIN pada siklus CBR.

Basis kasus = kasus rujukan awal (``data/dataset.py``) + kasus yang disimpan
pengguna lewat Retain. Kasus tersimpan ditulis ke berkas JSON sehingga tetap
ada setelah aplikasi dimuat ulang dan ikut dipakai pada Retrieve berikutnya.

Hanya pustaka standar Python yang dipakai. Identitas pasien (nama, usia,
jenis kelamin) sengaja tidak pernah disimpan: yang tersimpan hanya pola gejala
dan grade akhirnya.
"""

import datetime
import json
import os
import tempfile
import threading

from utils.validation import validasi_vektor

BERKAS_DEFAULT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "basis_kasus.json",
)

_KUNCI = threading.Lock()


def _path(path):
    return path or os.environ.get("CEKDBD_BASIS_KASUS") or BERKAS_DEFAULT


def _baca(path):
    try:
        with open(path, encoding="utf-8") as berkas:
            isi = json.load(berkas)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError):
        # Berkas rusak dianggap kosong agar aplikasi tetap bisa dipakai.
        return {}
    return isi if isinstance(isi, dict) else {}


def _tulis(path, isi):
    """Menulis secara atomik: tulis ke berkas sementara, lalu ganti."""
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    fd, sementara = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as berkas:
            json.dump(isi, berkas, ensure_ascii=False, indent=2)
        os.replace(sementara, path)
    except BaseException:
        if os.path.exists(sementara):
            os.remove(sementara)
        raise


def kasus_tersimpan(dataset, path=None):
    """Kasus hasil Retain untuk ``dataset`` (daftar dict)."""
    with _KUNCI:
        isi = _baca(_path(path))
    daftar = isi.get(dataset.key, [])
    return [k for k in daftar if isinstance(k, dict)]


def muat_basis(dataset, path=None):
    """Seluruh basis kasus: rujukan awal diikuti kasus tersimpan."""
    basis = []
    for kasus in dataset.kasus_lama:
        kasus["sumber"] = "rujukan"
        basis.append(kasus)
    basis.extend(kasus_tersimpan(dataset, path))
    return basis


def jumlah_tersimpan(dataset, path=None):
    return len(kasus_tersimpan(dataset, path))


def _kode_baru(dataset, grade, tersimpan):
    """Kode kasus baru, mis. ``DHF2-K1`` untuk grade DHF2."""
    kode_grade = None
    for kode, nama in zip(dataset.kode_kasus, dataset.nama_kasus):
        if nama == grade:
            kode_grade = kode
            break
    if kode_grade is None:
        raise ValueError(f"Grade '{grade}' tidak dikenal.")

    nomor = 0
    awalan = f"{kode_grade}-K"
    for kasus in tersimpan:
        kode = str(kasus.get("kode", ""))
        if kode.startswith(awalan) and kode[len(awalan):].isdigit():
            nomor = max(nomor, int(kode[len(awalan):]))
    return f"{awalan}{nomor + 1}"


def retain(dataset, kasusbaru, revisi, path=None, waktu=None):
    """Menyimpan kasus baru beserta solusi akhirnya ke basis kasus.

    ``revisi`` adalah hasil ``core.cbr.revise``. Kasus yang polanya sama persis
    dengan kasus lama bergrade sama tidak disimpan lagi (tidak menambah
    pengetahuan). Mengembalikan ``{"status": "disimpan" | "duplikat",
    "kasus": {...}}``.
    """
    validasi_vektor(kasusbaru, [], dataset.jumlah_atribut)
    if not any(nilai != 0 for nilai in kasusbaru):
        raise ValueError("Kasus tanpa gejala tidak dapat disimpan.")

    grade = revisi["grade_final"]

    with _KUNCI:
        lokasi = _path(path)
        isi = _baca(lokasi)
        tersimpan = [k for k in isi.get(dataset.key, []) if isinstance(k, dict)]

        basis = dataset.kasus_lama + tersimpan
        for kasus in basis:
            if kasus["nama"] == grade and list(kasus["vektor"]) == list(kasusbaru):
                return {"status": "duplikat", "kasus": kasus}

        waktu = waktu or datetime.datetime.now().replace(microsecond=0)
        kasus = {
            "kode": _kode_baru(dataset, grade, tersimpan),
            "nama": grade,
            "vektor": list(kasusbaru),
            "sumber": "retain",
            "direvisi": bool(revisi["direvisi"]),
            "catatan": revisi.get("catatan", ""),
            "dibuat": waktu.isoformat(),
        }
        tersimpan.append(kasus)
        isi[dataset.key] = tersimpan
        _tulis(lokasi, isi)

    return {"status": "disimpan", "kasus": kasus}
