# Dokumentasi Perhitungan

## 1. Rumus yang dipakai

Dua vektor dibandingkan:

- `A` = kasus baru
- `B` = kasus lama

```text
dot product  = Σ (A[j] × B[j])
ΣA²          = Σ (A[j]²)
ΣB²          = Σ (B[j]²)
|A|          = √(ΣA²)
|B|          = √(ΣB²)

Cosine(A, B) = dot product / (|A| × |B|)
Persentase   = Cosine × 100%
```

Jika `|A| × |B| = 0`, maka `Cosine = 0.0` sesuai kode Python yang diberikan.
Pembulatan hanya untuk tampilan; perankingan memakai nilai cosine sebelum dibulatkan.

Implementasi terdapat pada `core/cosine_similarity.py`:

```python
def cosine_similarity(kasusbaru, kasus):
    dot = 0
    kuadrat_kasusbaru = 0
    kuadrat_kasus = 0

    for j in range(len(kasusbaru)):
        dot += kasusbaru[j] * kasus[j]
        kuadrat_kasusbaru += kasusbaru[j] ** 2
        kuadrat_kasus += kasus[j] ** 2

    panjang_kasusbaru = kuadrat_kasusbaru ** 0.5
    panjang_kasus = kuadrat_kasus ** 0.5

    if panjang_kasusbaru * panjang_kasus == 0:
        cosine = 0.0
    else:
        cosine = dot / (panjang_kasusbaru * panjang_kasus)

    return dot, cosine
```

## 2. Alur CBR

`core/cbr.py` melakukan langkah berikut untuk setiap kasus lama:

1. Ambil vektor kasus baru dan vektor kasus lama.
2. Hitung dot product, jumlah kuadrat, panjang vektor, dan cosine.
3. Simpan kode kasus, nama kasus, dot product, semua komponen perhitungan,
   cosine, dan persentase.
4. Urutkan hasil dari cosine tertinggi.
5. Pilih kasus pertama pada urutan tersebut sebagai rekomendasi.

## 3. Contoh perhitungan DHF

Kasus baru:

```text
A = [1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]
```

### DHF1

```text
B       = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]
dot     = 1 + 0 + 0 + 0 + 0 + 0 + 0 + 1 + 0 + 0 + 0 + 1 + 1 + 1 = 5
ΣA²     = 8
ΣB²     = 5
|A|     = √8 = 2,828427
|B|     = √5 = 2,236068
cosine  = 5 / (2,828427 × 2,236068)
        = 5 / 6,324555
        = 0,790569
persen  = 79,06%
```

### Seluruh hasil DHF

| Kasus | Nama | Dot | ΣA² | ΣB² | \|A\| | \|B\| | Cosine | Persentase |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| DHF1 | Demam Berdarah Grade I | 5 | 8 | 5 | 2,828427 | 2,236068 | 0,7906 | 79,06% |
| DHF2 | Demam Berdarah Grade II | 6 | 8 | 6 | 2,828427 | 2,449490 | 0,8660 | 86,60% |
| DHF3 | Demam Berdarah Grade III | 6 | 8 | 7 | 2,828427 | 2,645751 | 0,8018 | 80,18% |
| DHF4 | Demam Berdarah Grade IV | 4 | 8 | 6 | 2,828427 | 2,449490 | 0,5774 | 57,74% |

**Hasil:** kasus baru paling mirip dengan **DHF2 — Demam Berdarah Grade II**
(0,8660 / 86,60%).

## 4. Contoh perhitungan P006

Kasus baru dari kode yang diberikan:

```text
A = [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
```

### P004 — Tumor Lambung

```text
B       = [0, 0, 0, 0, 0, 5, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0]
dot     = (0×0) + ... + (1×5) + (1×5) + ... + (1×1) + ... + (1×5) + ... = 16
ΣA²     = 5
ΣB²     = 76
|A|     = √5  = 2,236068
|B|     = √76 = 8,717798
cosine  = 16 / (2,236068 × 8,717798)
        = 16 / 19,493589
        = 0,820783
persen  = 82,08%
```

### Seluruh hasil P006

| Kasus | Nama | Dot | ΣA² | ΣB² | \|A\| | \|B\| | Cosine | Persentase |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P001 | Gastritis | 2 | 5 | 61 | 2,236068 | 7,810250 | 0,1145 | 11,45% |
| P002 | Maag | 0 | 5 | 36 | 2,236068 | 6,000000 | 0,0000 | 0,00% |
| P003 | Kanker Lambung | 4 | 5 | 64 | 2,236068 | 8,000000 | 0,2236 | 22,36% |
| P004 | Tumor Lambung | 16 | 5 | 76 | 2,236068 | 8,717798 | 0,8208 | 82,08% |
| P005 | GERD | 0 | 5 | 25 | 2,236068 | 5,000000 | 0,0000 | 0,00% |

**Hasil:** kasus baru P006 paling mirip dengan **P004 — Tumor Lambung**
(0,8208 / 82,08%).

## 5. Ranking

Peringkat dibuat dari nilai cosine tertinggi.

### DHF

1. DHF2 — 0,8660 (86,60%)
2. DHF3 — 0,8018 (80,18%)
3. DHF1 — 0,7906 (79,06%)
4. DHF4 — 0,5774 (57,74%)

### P006

1. P004 — 0,8208 (82,08%)
2. P003 — 0,2236 (22,36%)
3. P001 — 0,1145 (11,45%)
4. P002 — 0,0000 (0,00%)
5. P005 — 0,0000 (0,00%)

Untuk nilai cosine yang sama, urutan dataset awal tetap dipertahankan karena
`sorted` pada Python bersifat stabil.

## 6. Kasus khusus dan validasi

- **Vektor kasus baru semua nol:** dot product dan kedua panjang vektor dihitung
  seperti biasa. Karena penyebutnya nol, cosine ditetapkan `0.0`.
- **Jumlah atribut berbeda:** `validasi_vektor()` melempar `ValueError` sebelum
  perhitungan dijalankan.
- **Nilai bukan angka:** juga ditolak oleh `validasi_vektor()`.
- **Pembulatan:** `round`/format hanya dipakai pada teks tampilan dan tabel,
  tidak pada nilai yang dipakai untuk mencari peringkat.

## 7. Pengujian aktual

Perintah:

```bash
python -m unittest discover -s tests -v
```

Nilai yang diuji:

- DHF: dot `[5, 6, 6, 4]`, cosine `[0,7905694150, 0,8660254038, 0,8017837257, 0,5773502692]`.
- P006: dot `[2, 0, 4, 16, 0]`, cosine `[0,1145196669, 0, 0,2236067977, 0,8207826817, 0]`.
- Vektor nol menghasilkan cosine `0.0`.
- Kasus terbaik DHF = `DHF2`, P006 = `P004`.
- Validasi menolak jumlah atribut yang tidak sesuai dan nilai bukan angka.
- Fungsi `buat_kasus_baru()` menghasilkan vektor contoh DHF jika gejala
  G1, G2, G5, G8, G9, G12, G13, dan G14 dipilih.

## 8. Penyajian untuk pengguna umum

Antarmuka sengaja disederhanakan menjadi tiga langkah: data diri, pilih gejala,
lalu hasil. Data diri tidak masuk ke vektor perhitungan. Pada halaman hasil,
nilai cosine ditampilkan sebagai persentase kemiripan dengan satu angka desimal
agar mudah dibaca, misalnya **86,6%**.

Kata "kemungkinan" pada tampilan dipakai dalam arti "seberapa mirip gejala dengan
kasus rujukan", bukan probabilitas medis. Penjelasan ini ditampilkan langsung di
bawah hasil agar pengguna tidak salah menafsirkan. Detail dot product, panjang
vektor, dan rumus tetap tersedia tetapi disembunyikan di dalam expander opsional.
