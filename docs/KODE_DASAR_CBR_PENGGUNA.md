# Kode Dasar CBR — Acuan Penulis

Berkas ini berisi kode Cosine Similarity yang diberikan Penulis dan menjadi dasar kesetaraan implementasi di `core/cosine_similarity.py`.

Kode di bawah disalin apa adanya dari pesan Penulis. Dua baris komentar setelah `def cosine_similarity(...)` sengaja tidak diindentasi sesuai teks asli. Pada implementasi project, komentar sejenis berada di dalam badan fungsi sehingga tetap valid secara sintaks Python.

```python
# ============================================================
# PROGRAM CASE BASED REASONING (CBR)
# PERHITUNGAN COSINE SIMILARITY
# ============================================================


# 1. DATA KASUS BARU
kasusbaru = [
    0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
    1, 0, 0, 0, 0, 0, 0, 1, 0
]

# 2. DATA KASUS LAMA
kasus_lama = [
    [0, 0, 0, 0, 0, 0, 0, 3, 1, 5, 1, 0, 0, 0, 0, 5, 0, 0, 0],  # P001 - Gastritis
    [1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0],  # P002 - Maag
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 3, 5, 0, 0, 5, 0, 1, 0, 0],  # P003 - Kanker Lambung
    [0, 0, 0, 0, 0, 5, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],  # P004 - Tumor Lambung
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]   # P005 - GERD
]


# 3. FUNGSI COSINE SIMILARITY
def cosine_similarity(kasusbaru, kasuslama):
# tahap pertama saya membuatkan satu fungsi dengan nama cosine_similarity dengan
# parameter kasusbaru dan kasus lama


    dot = 0
    # digunakan untuk menyimpan data hasil dari dot perhitungan pada syntac dibawah
    kuadrat_baru = 0
    kuadrat_lama = 0

    for i in range(len(kasusbaru)):
        dot += kasusbaru[i] * kasuslama[i]
        kuadrat_baru += kasusbaru[i] ** 2
        kuadrat_lama += kasuslama[i] ** 2

    panjang_baru = kuadrat_baru ** 0.5
    panjang_lama = kuadrat_lama ** 0.5

    penyebut = panjang_baru * panjang_lama

    if penyebut == 0:
        cosine = 0.0
    else:
        cosine = dot / penyebut

    return dot, cosine


# 4. PROSES PERBANDINGAN KASUS
hasil = []

for i, kasus in enumerate(kasus_lama):

    dot, cosine = cosine_similarity(kasusbaru, kasus)

    hasil.append(cosine)

    print(f"Kasus Baru dibandingkan dengan P{i + 1:03d}")
    print(f"Dot Product       : {dot}")
    print(f"Cosine Similarity : {cosine:.4f}")
    print(f"Persentase        : {cosine * 100:.2f}%")
    print("-" * 45)


# 5. MENENTUKAN KASUS DENGAN KEMIRIPAN TERTINGGI
indeks_tertinggi = hasil.index(max(hasil))
nilai_tertinggi = hasil[indeks_tertinggi]

print("\n" + "=" * 45)
print("                  KESIMPULAN")
print("=" * 45)

print(f"Kasus paling mirip : P{indeks_tertinggi + 1:03d}")
print(f"Cosine Similarity  : {nilai_tertinggi:.4f}")
print(f"Persentase         : {nilai_tertinggi * 100:.2f}%")

print("=" * 45)
```

## Kesetaraan dengan implementasi project

| Kode acuan Penulis | Implementasi project | Keterangan |
|---|---|---|
| `kuadrat_baru`, `kuadrat_lama` | `kuadrat_kasusbaru`, `kuadrat_kasus` | Hanya beda nama variabel |
| `panjang_baru`, `panjang_lama` | `panjang_kasusbaru`, `panjang_kasus` | Hanya beda nama variabel |
| `penyebut == 0` | `panjang_kasusbaru * panjang_kasus == 0` | Secara matematis ekuivalen |
| `hasil.index(max(hasil))` | `kasus_terbaik()` dengan loop dan `>` | Project lebih eksplisit |
| Tidak ada pengurutan | `sorted(..., reverse=True)` di `urutkan_hasil()` | Ditambahkan untuk ranking UI |
| `kasus_lama` berupa list of list | `kasus_lama` berupa list of dict | Project menyimpan `kode`, `nama`, dan `vektor` |

Nilai yang dihasilkan tetap sama. Untuk contoh P006, dot product `[2, 0, 4, 16, 0]` dan kasus terbaik `P004 — Tumor Lambung`.
