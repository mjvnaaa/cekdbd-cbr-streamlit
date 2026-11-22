from .cosine_similarity import hitung_detail

# Kemiripan terbaik di bawah ambang ini ditandai "perlu ditinjau" pada tahap Revise.
AMBANG_YAKIN = 0.80


def buat_kasus_baru(terpilih, atribut):
    kasusbaru = []

    for a in atribut:
        kasusbaru.append(1 if a["kode"] in terpilih else 0)

    return kasusbaru


def hitung_cbr(kasusbaru, kasus_lama):
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
    return sorted(hasil, key=lambda item: item["cosine"], reverse=True)


def kasus_terbaik(hasil):
    if not hasil:
        return None

    terbaik = hasil[0]

    for item in hasil[1:]:
        if item["cosine"] > terbaik["cosine"]:
            terbaik = item

    return terbaik


# ============================================================
# TAHAP 2: REUSE - memakai solusi kasus lama yang paling mirip
# ============================================================

def reuse(hasil):
    """Mengusulkan solusi (grade) dari kasus terbaik hasil Retrieve.

    Mengembalikan dict usulan. ``grade`` bernilai ``None`` bila tidak ada
    kasus lama yang mirip sama sekali (cosine 0), sehingga solusi harus
    ditentukan lewat tahap Revise.
    """
    terbaik = kasus_terbaik(hasil)
    if terbaik is None:
        return None

    ada_kemiripan = terbaik["cosine"] > 0

    # Grade lain dengan kemiripan sama persis membuat usulan ambigu.
    seri = False
    for item in hasil:
        if item["kode"] != terbaik["kode"] and item["nama"] != terbaik["nama"]:
            if item["cosine"] == terbaik["cosine"]:
                seri = True

    return {
        "kode_kasus": terbaik["kode"],
        "grade": terbaik["nama"] if ada_kemiripan else None,
        "cosine": terbaik["cosine"],
        "persentase": terbaik["persentase"],
        "perlu_ditinjau": (not ada_kemiripan)
        or terbaik["cosine"] < AMBANG_YAKIN
        or seri,
    }


# ============================================================
# TAHAP 3: REVISE - meninjau dan memperbaiki solusi usulan
# ============================================================

def revise(usulan, grade_final, daftar_grade, catatan=""):
    """Menetapkan solusi akhir setelah ditinjau pengguna/pakar.

    ``grade_final`` harus salah satu dari ``daftar_grade``. Solusi dianggap
    direvisi bila berbeda dari grade yang diusulkan tahap Reuse.
    """
    if usulan is None:
        raise ValueError("Belum ada solusi usulan untuk ditinjau.")

    if not grade_final:
        raise ValueError("Pilih grade akhir terlebih dahulu.")

    if grade_final not in daftar_grade:
        raise ValueError(f"Grade '{grade_final}' tidak dikenal.")

    return {
        "grade_usulan": usulan["grade"],
        "grade_final": grade_final,
        "direvisi": grade_final != usulan["grade"],
        "catatan": str(catatan or "").strip(),
    }
