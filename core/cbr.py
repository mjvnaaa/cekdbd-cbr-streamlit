"""Tahap Case-Based Reasoning (CBR) berbasis Cosine Similarity."""

from .cosine_similarity import hitung_detail


def buat_kasus_baru(terpilih, atribut):
    """Membangun vektor kasus baru dari daftar kode atribut yang dipilih.

    Dipakai untuk dataset DHF: 1 bila kode gejala dipilih, 0 bila tidak.
    Logika ini setara dengan ``buatKasusBaru`` pada ``js/cbr.js``.
    """

    kasusbaru = []
    for a in atribut:
        kasusbaru.append(1 if a["kode"] in terpilih else 0)
    return kasusbaru


def hitung_cbr(kasusbaru, kasus_lama):
    """Membandingkan kasus baru dengan setiap kasus lama.

    Setiap kasus lama berbentuk dict dengan kunci ``kode``, ``nama``, dan
    ``vektor``. Nilai ``persentase`` sengaja tidak dibulatkan di sini;
    pembulatan hanya dilakukan saat ditampilkan.
    """

    hasil = []

    for kasus in kasus_lama:
        detail = hitung_detail(kasusbaru, kasus["vektor"])
        hasil.append(
            {
                "kode": kasus["kode"],
                "nama": kasus["nama"],
                "vektor": list(kasus["vektor"]),
                "dot": detail["dot"],
                "kuadrat_kasusbaru": detail["kuadrat_kasusbaru"],
                "kuadrat_kasus": detail["kuadrat_kasus"],
                "panjang_kasusbaru": detail["panjang_kasusbaru"],
                "panjang_kasus": detail["panjang_kasus"],
                "penyebut": detail["penyebut"],
                "cosine": detail["cosine"],
                "persentase": detail["cosine"] * 100,
            }
        )

    return hasil


def urutkan_hasil(hasil):
    """Mengurutkan hasil dari cosine similarity tertinggi.

    ``sorted`` bersifat stabil, sehingga jika dua nilai sama, urutan dataset
    awal tetap dipertahankan.
    """

    return sorted(hasil, key=lambda item: item["cosine"], reverse=True)


def kasus_terbaik(hasil):
    """Mengambil kasus dengan cosine similarity tertinggi.

    Jika terdapat nilai sama, kasus yang lebih awal pada dataset yang dipilih.
    """

    if not hasil:
        return None

    terbaik = hasil[0]
    for item in hasil[1:]:
        if item["cosine"] > terbaik["cosine"]:
            terbaik = item
    return terbaik
