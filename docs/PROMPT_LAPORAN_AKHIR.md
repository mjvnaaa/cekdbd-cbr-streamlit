# PROMPT SIAP PAKAI — Laporan Proyek Akhir SPK (CBR + Cosine Similarity)

> **Cara pakai:** Salin seluruh isi file ini ke AI yang akan Anda minta menyusun laporan proyek akhir.
> Lampirkan juga berkas-berkas di dalam `Konteks-Proyek-SPK-CBR.zip` sebagai bahan referensi.
> Prompt ini sudah ditulis agar AI tidak mengarang fitur yang belum ada di project.

---

## 1. Peran dan tugas

Anda adalah asisten akademik yang membantu **Moh. Jevon Attaillah** menyusun **laporan proyek akhir mata kuliah Sistem Pendukung Keputusan (SPK)**.

Judul proyek:

**CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus Menggunakan Case-Based Reasoning dan Cosine Similarity**

Tugas Anda:

1. Menyusun laporan lengkap, sistematis, dan berbahasa Indonesia formal akademik.
2. Menjelaskan **seluruh alur perhitungan CBR dan Cosine Similarity secara manual**, bukan sekadar menyebut namaLibrary.
3. Menunjukkan bahwa perhitungan inti ditulis dengan perulangan dan operasi matematika dasar Python.
4. Menyertakan contoh perhitungan angka nyata yang sudah diverifikasi oleh test project.
5. Memisahkan secara tegas antara **fitur yang sudah implemented** dan **rencana pengembangan**.

Gunakan format **Markdown** dengan heading bertingkat, tabel, dan blok kode. Penulisan memakai kata ganti **"Penulis"**, bukan "saya" atau "kamu".

---

## 2. Identitas proyek

| Informasi | Isi |
|---|---|
| Nama | Moh. Jevon Attaillah |
| NIM | 362458302035 |
| Kelas | TRPL 3D |
| Program studi | Rekayasa Perangkat Lunak |
| Mata kuliah | Sistem Pendukung Keputusan (SPK) |
| Judul aplikasi | CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus Menggunakan CBR dan Cosine Similarity |
| Topik data | Kemiripan grade Demam Berdarah (DHF) |
| Referensi utama | Jatmiko, Junaedi, dan Imrona (2017), *e-Proceeding of Engineering*, 4(2), 3269–3276 |
| State Git saat audit | Bersih; hanya penambahan berkas konteks, tidak ada perubahan logika |

**Penting:** Angka akurasi **92%** yang muncul di referensi adalah hasil penelitian Jatmiko dkk. (2017), **bukan** akurasi aplikasi ini. Jangan pernah menulis sebaliknya.

---

## 3. Batasan yang WAJIB dipatuhi

1. **Logika inti CBR/Cosine Similarity harus dinyatakan sebagai implementasi manual.**
   - Dot product: `dot += kasusbaru[j] * kasus[j]`
   - Jumlah kuadrat: `kuadrat += nilai ** 2`
   - Panjang vektor: `kuadrat ** 0.5`
   - Cosine: `dot / (panjang_a * panjang_b)`
   - Kasus terbaik: perbandingan `>` dengan perulangan manual.

2. **Dilarang mengatakan/menulis bahwa project memakai NumPy, Pandas, scikit-learn, SciPy, atau library machine learning lain untuk perhitungan.**
   - `requirements.txt` hanya berisi `streamlit>=1.39.0`.
   - Modul standar Python yang dipakai: `dataclasses`, `typing`, `numbers`, `unittest`, `html`, `re`, `datetime`.

3. **Pandas/OpenPyXL hanya diperbolehkan untuk membaca data Excel, bukan menghitung.**
   - `sqlite3` (standard library) boleh dipakai untuk database.
   - Namun **status saat ini: database belum diimplementasikan**. Data masih berupa konstanta di `data/dataset.py`.
   - Di laporan, sebut integrasi database hanya di **Bab V / Rekomendasi**, jangan di Bab III–IV seolah sudah berjalan.

4. **Jangan mengubah rumus atau mengganti metode.**
   - Cosine Similarity tidak diganti dengan Euclidean, Jaccard, atau metode lain.

5. **Jangan mengarang data yang tidak ada di project.**
   - Nama dosen pembimbing, fakultas, tanggal ujian, dan nilai akurasi aplikasi tidak tersedia. Jika diperlukan, tulis `[data tidak tersedia]` atau tanyakan kepada Penulis.

6. **Jangan menyembunyikan temuan audit.**
   - Sertakan secara jujur bahwa `sorted()` dipakai untuk ranking, dan bahwa `hitung_detail()` saat ini menghitung ulang kuadrat. Keduanya bukan pelanggaran rumus, tetapi dibahas sebagai catatan perbaikan.

---

## 4. Arsitektur dan peta file

```text
Tugas-Akhir-Streamlit/
├── app.py                         # Entry point Streamlit + navigasi halaman
├── core/
│   ├── __init__.py
│   ├── cosine_similarity.py       # Rumus manual + detail komponen perhitungan
│   └── cbr.py                     # Pembandingan kasus, ranking, kasus terbaik
├── data/
│   ├── __init__.py
│   └── dataset.py                 # Dataset DHF (14 atribut) dan P006 (19 atribut)
├── utils/
│   ├── __init__.py
│   └── validation.py              # Validasi vektor, pasien, dan pilihan gejala
├── components/
│   ├── __init__.py
│   ├── dashboard.py               # Halaman awal / penjelasan metode
│   ├── input_form.py              # Form identitas + pilihan gejala + trigger hitung CBR
│   ├── info_view.py               # Identitas akademik, referensi, tampilan dataset
│   ├── layout.py                  # Navbar, stepper, footer, label grade
│   ├── result_view.py             # Lembar hasil dan grafik perbandingan
│   └── theme.py                   # CSS, ikon, dan escaping HTML
├── tests/
│   └── test_cosine_similarity.py  # 10 unittest untuk logika dan validasi
├── docs/
│   ├── README.md                  # Panduan jalankan & deploy aplikasi
│   ├── AUDIT_PROYEK_LAMA.md       # Audit project HTML/JS sebelum migrasi
│   ├── DOKUMENTASI_PERHITUNGAN.md # Penelusuran angka perhitungan
│   ├── PERBANDINGAN_JS_PYTHON.md  # Perbandingan implementasi lama dan baru
│   ├── AUDIT_CBR_IMPLEMENTASI.md  # Audit 21 November 2026 (file baru)
│   └── KODE_DASAR_CBR_PENGGUNA.md # Kode acuan asli dari Penulis (file baru)
├── requirements.txt
├── PROMPT_LAPORAN_AKHIR.md        # File prompt ini (file baru)
└── MANIFEST_KONTEKS.md            # Daftar isi paket konteks (file baru)
```

Alur runtime ringkas:

```text
app.py
  -> components/input_form.py
       -> buat_kasus_baru(pilih, atribut)     [core/cbr.py]
       -> validasi_vektor(...)                 [utils/validation.py]
       -> hitung_cbr(kasusbaru, kasus_lama)    [core/cbr.py]
            -> hitung_detail(...)              [core/cosine_similarity.py]
                 -> cosine_similarity(...)     [core/cosine_similarity.py]
       -> urutkan_hasil(...) + kasus_terbaik(...) [core/cbr.py]
  -> components/result_view.py (tampilkan hasil)
```

Identitas pasien (nama, usia, jenis kelamin) **hanya untuk kop laporan**, tidak ikut dihitung.

---

## 5. Rumus dan bukti implementasi manual

Rumus yang dipakai:

```text
dot(A, B)   = Σ (A[j] × B[j])
ΣA²         = Σ (A[j]²)
ΣB²         = Σ (B[j]²)
|A|         = √(ΣA²)
|B|         = √(ΣB²)
Cosine(A,B) = dot(A, B) / (|A| × |B|)
Persentase  = Cosine × 100%
```

Jika `|A| × |B| = 0`, maka `Cosine = 0.0`.

### Kode aktual di `core/cosine_similarity.py`

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

### Kode aktual di `core/cbr.py`

```python
def buat_kasus_baru(terpilih, atribut):
    kasusbaru = []
    for a in atribut:
        kasusbaru.append(1 if a["kode"] in terpilih else 0)
    return kasusbaru


def hitung_cbr(kasusbaru, kasus_lama):
    hasil = []
    for kasus in kasus_lama:
        detail = hitung_detail(kasusbaru, kasus["vektor"])
        hasil.append({
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
        })
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
```

Penjelasan yang harus muncul di Bab IV:

- `for j in range(len(kasusbaru))` membaca dua vektor posisi demi posisi.
- `dot`, `kuadrat_kasusbaru`, dan `kuadrat_kasus` diakumulasikan di loop yang sama.
- `** 0.5` adalah akar kuadrat dengan operator pangkat Python, bukan `math.sqrt`.
- `kasus_terbaik()` memakai perulangan dan operator `>`, lebih eksplisit daripada `max()` pada kode acuan.
- `sorted()` hanya mengurutkan nilai cosine yang sudah jadi; tidak menghitung cosine.

---

## 6. Kode acuan asli dari Penulis

Kode berikut adalah dasar yang dipelajari Penulis dan menjadi acuan kesetaraan implementasi. Salin/ringkas pada **Lampiran A** laporan. Versi lengkap juga tersedia di `docs/KODE_DASAR_CBR_PENGGUNA.md`.

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

Catatan untuk AI: dua baris komentar setelah `def` sengaja dipertahankan apa adanya sesuai pesan Penulis. Pada implementasi project, komentar sejenis berada di dalam badan fungsi sehingga tetap valid secara sintaks Python.

---

## 7. Dataset yang dipakai

| Dataset | Jumlah atribut | Kasus lama | Nilai | Status di UI |
|---|---:|---:|---|---|
| DHF | 14 (G1–G14) | 4 (DHF1–DHF4) | 0 / 1 | Dipakai sebagai alur utama aplikasi |
| P006 | 19 (F1–F19) | 5 (P001–P005) | kasus lama 0/1/3/5; kasus baru contoh 0/1 | Tersimpan di `data/`, `core/`, dan `tests/`, belum ditampilkan di UI |

Sumber DHF: Jatmiko, Junaedi, dan Imrona (2017), Tabel 2-1 sampai 2-3.  
Sumber P006: kode Python yang diberikan Penulis. Nama atribut tidak tersedia, sehingga memakai kode netral `F1`–`F19`; **jangan mengarang nama gejala**.

Contoh kasus baru DHF:

```text
[1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]
```

Contoh kasus baru P006:

```text
[0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
```

---

## 8. Hasil pengujian yang sudah diverifikasi

Perintah:

```bash
python -m unittest discover -s tests -v
```

Hasil: **10 test lulus (OK)**.

Nilai acuan yang harus dipakai di Bab IV:

| Dataset | Dot product per kasus | Cosine per kasus | Kasus terbaik |
|---|---|---|---|
| DHF | `[5, 6, 6, 4]` | `[0.7905694150, 0.8660254038, 0.8017837257, 0.5773502692]` | DHF2 — Grade II |
| P006 | `[2, 0, 4, 16, 0]` | `[0.1145196669, 0.0, 0.2236067977, 0.8207826817, 0.0]` | P004 — Tumor Lambung |

Contoh penelusuran angka yang wajib ditulis:

**DHF vs DHF2**

```text
dot        = 6
ΣA²        = 8
ΣB²        = 6
|A|        = √8 = 2.8284
|B|        = √6 = 2.4495
cosine     = 6 / (2.8284 × 2.4495) = 0.8660
persentase = 86,60%
```

**P006 vs P004**

```text
dot        = 16
ΣA²        = 5
ΣB²        = 76
|A|        = √5  = 2.2361
|B|        = √76 = 8.7178
cosine     = 16 / (2.2361 × 8.7178) = 0.8208
persentase = 82,08%
```

Gunakan koma sebagai pemisah desimal dalam teks laporan Bahasa Indonesia, tetapi boleh memakai titik di dalam blok kode.

---

## 9. Ringkasan audit implementasi (sertakan di Bab IV)

| No | Pertanyaan audit | Verdict | Bukti |
|---|---|---|---|
| 1 | Dot product dihitung manual dengan perulangan dan perkalian? | Ya | `core/cosine_similarity.py`, loop `for j in range(...)` |
| 2 | Panjang vektor dihitung dengan penjumlahan kuadrat dan akar manual? | Ya | `kuadrat += nilai ** 2`, lalu `** 0.5` |
| 3 | Cosine dihitung dengan operasi matematika dasar? | Ya | `dot / (panjang_a * panjang_b)` + penanganan nol |
| 4 | Perbandingan kasus dan penentuan tertinggi memakai logika dasar Python? | Ya | loop di `hitung_cbr()` dan `kasus_terbaik()`; ranking memakai `sorted()` bawaan |
| 5 | Ada library/fungsi yang mengambil alih perhitungan? | Tidak untuk rumus | `sorted()`, `sum()`, `max()/min()` hanya untuk ranking dan tampilan |

Temuan yang harus dibahas jujur di sub-bab "Pembahasan Audit":

1. **Integrasi database belum ada.** Data masih hard-code di `data/dataset.py`. Ini bukan kesalahan rumus, tetapi belum memenuhi target web dinamis + database.
2. **`hitung_detail()` menghitung ulang kuadrat.** `cosine_similarity()` sudah menghitung kuadrat, lalu `hitung_detail()` mengulangnya untuk keperluan tampilan. Hasilnya saat ini konsisten (terbukti test), tetapi rawan jika salah satu diubah.
3. **`sorted()` adalah built-in.** Bukan library dan tidak menghitung cosine. Jika dosen menginginkan pengurutan manual, bisa diganti bubble sort; sebut sebagai opsi, bukan keharusan.
4. **Detail perhitungan belum ditampilkan di UI.** `hitung_detail()` sudah menyediakan komponennya; disarankan ditambahkan expander "Lihat perhitungan CBR" di halaman hasil.

---

## 10. Struktur laporan yang diminta

Susun laporan dengan struktur berikut.

### Bab I — Pendahuluan

- Latar belakang: peran SPK, kasus DHF, alasan memakai CBR.
- Rumusan masalah (minimal 3 butir).
- Tujuan penelitian.
- Manfaat penelitian (Penulis, dosen, pengguna umum).
- Ruang lingkup: dua dataset, perhitungan kemiripan, antarmuka Streamlit.

### Bab II — Landasan Teori dan Studi Terkait

- Sistem Pendukung Keputusan.
- Case-Based Reasoning: siklus *Retrieve, Reuse, Revise, Retain*.
- Cosine Similarity: definisi, rumus, geometri vektor, keuntungan untuk data biner/berbobot.
- Demam Berdarah dan grade DHF.
- Studi terkait: Jatmiko dkk. (2017). Tekankan bahwa 92% adalah akurasi paper mereka.

### Bab III — Analisis dan Desain Sistem

- Analisis kebutuhan fungsional dan nonfungsional.
- Alur data: input gejala → vektor → perhitungan → ranking → laporan.
- Desain struktur folder dan tanggung jawab tiap modul.
- Desain vektor kasus (G1–G14 dan F1–F19).
- Pseudocode Manual Cosine Similarity dan CBR.
- Jelaskan batasan: database **belum** diimplementasikan. Jika perlu digambarkan, beri subtitle **"Rancangan Integrasi Database (Rencana)"**.

### Bab IV — Implementasi dan Pengujian

- Penjelasan env: Streamlit sebagai antarmuka, Python murni sebagai inti.
- Pembahasan baris per baris `core/cosine_similarity.py` dan `core/cbr.py`.
- Tabel komponen perhitungan (`dot`, `ΣA²`, `ΣB²`, `|A|`, `|B|`, `penyebut`, `cosine`).
- Contoh perhitungan DHF dan P006 seperti pada Bagian 8 prompt ini.
- Tampilan antarmuka: beranda, data diri, gejala, hasil, dataset.
- Tabel hasil pengujian unit test.
- Sub-bab **"Audit Kesesuaian dengan Kode Acuan"** memakai tabel Bagian 9.

### Bab V — Penutup dan Rekomendasi

- Kesimpulan: rumus terbukti manual, tidak ada library numerik, hasil test valid.
- Saran:
  1. integrasi `sqlite3`/OpenPyXL hanya sebagai pembaca data;
  2. satukan perhitungan di `hitung_detail()` agar satu sumber angka;
  3. opsional: ganti `sorted()` dengan bubble sort jika diperlukan untuk keperluan akademik;
  4. tambahkan expander detail perhitungan di `result_view.py`.
- Penutup singkat.

### Daftar Pustaka

- Jatmiko, A. D., Junaedi, D., & Imrona, M. (2017). Analisis dan Implementasi Sistem Pakar dengan Metode Case Based Reasoning dan Rule Based Reasoning. *e-Proceeding of Engineering*, 4(2), 3269–3276.
- Referensi tambahan tentang Streamlit dan Python bila diperlukan, sesuai format yang Anda pakai.

### Lampiran

- **Lampiran A:** Kode acuan Penulis (Bagian 6 prompt ini).
- **Lampiran B:** Kode lengkap `core/cosine_similarity.py` dan `core/cbr.py`.
- **Lampiran C:** Tabel perhitungan lengkap DHF dan P006.
- **Lampiran D:** Daftar file dalam paket konteks (sesuai `MANIFEST_KONTEKS.md`).

---

## 11. Gaya bahasa dan format

- Gunakan Bahasa Indonesia formal: "Penulis", "sistem", "aplikasi", "perhitungan", "dihasilkan".
- Hindari "saya", "kamu", "kita", dan bahasa percakapan.
- Istilah yang konsisten: **kasus baru**, **kasus lama**, **vektor**, **dot product**, **panjang vektor**, **cosine similarity**, **persentase kemiripan**.
- Gunakan penomoran Tabel dan Gambar secara konsisten, misalnya "Tabel 4.1 Hasil Perhitungan DHF".
- Sertakan minimal **3 tabel** dan **3 blok kode**.
- Panjang target: sekitar **6.000–9.000 kata** atau 20–30 halaman jika dikonversi ke document. Boleh disesuaikan bila Penulis memberi batas berbeda.
- Jangan menambahkan fitur, modul, atau angka yang tidak ada di dalam paket konteks ini.

---

## 12. Instruksi awal untuk AI

Mulai jawaban Anda dengan:

```text
# Laporan Proyek Akhir Sistem Pendukung Keputusan
## CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus Menggunakan CBR dan Cosine Similarity

Nama: Moh. Jevon Attaillah
NIM: 362458302035
Mata kuliah: Sistem Pendukung Keputusan (SPK)
Program Studi: Rekayasa Perangkat Lunak
```

Kemudian lanjutkan dengan **Daftar Isi**, lalu **Bab I**, dan seterusnya.

Jika ada informasi yang tidak tersedia di paket konteks, **tanyakan kepada Penulis**, jangan mengarang jawaban.
