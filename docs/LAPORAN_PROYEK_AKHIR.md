# Laporan Proyek Akhir Sistem Pendukung Keputusan

## CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus Menggunakan Case-Based Reasoning dan Cosine Similarity

| Keterangan | Isi |
|---|---|
| Nama | Moh. Jevon Attaillah |
| NIM | 362458302035 |
| Kelas | TRPL 3D |
| Program Studi | Rekayasa Perangkat Lunak |
| Mata Kuliah | Sistem Pendukung Keputusan (SPK) |
| Topik | Kemiripan kasus Demam Berdarah (DHF) |
| Referensi utama | Jatmiko, Junaedi, dan Imrona (2017) |

---

## Pendahuluan

### 1.1 Latar Belakang

Sistem Pendukung Keputusan (SPK) merupakan sistem informasi yang membantu pengguna mengambil keputusan dengan menyajikan analisis, perbandingan, atau rekomendasi. Salah satu pendekatan yang relevan untuk kasus diagnostik adalah **Case-Based Reasoning (CBR)**, yaitu metode yang menyelesaikan masalah baru dengan mencari kasus lama yang paling mirip.

Dalam proyek ini, CBR diterapkan untuk mencocokkan pola gejala pasien dengan empat kasus rujukan grade Demam Berdarah (DHF). Kemiripan dihitung memakai **Cosine Similarity**, karena data gejala direpresentasikan sebagai vektor biner maupun vektor berbobot. Cosine Similarity mengukur kesamaan arah dua vektor sehingga cocok untuk membandingkan pola gejala, bukan besaran absolutnya.

Aplikasi diberi nama **CekDBD** dan dibangun dengan Streamlit. Sesuai ketentuan mata kuliah, perhitungan inti tidak boleh diserahkan kepada library seperti NumPy, Pandas, atau scikit-learn. Oleh karena itu, seluruh proses dot product, penjumlahan kuadrat, perhitungan akar, cosine similarity, dan penentuan kasus terbaik ditulis langsung dengan perulangan dan operasi matematika dasar Python. Hal ini dilakukan agar Penulis mampu menjelaskan serta mempertanggungjawabkan setiap baris kode ketika diperiksa.

Dataset utama berasal dari penelitian Jatmiko, Junaedi, dan Imrona (2017) yang memuat 14 gejala dan 4 kasus DHF. Sebagai bahan perbandingan tambahan, project juga menyimpan dataset P006 dari kode contoh yang diberikan, dengan 19 atribut berbobot.

### 1.2 Rumusan Masalah

Berdasarkan latar belakang tersebut, rumusan masalah proyek ini adalah:

1. Bagaimana merepresentasikan gejala pasien sebagai vektor kasus baru?
2. Bagaimana menghitung dot product, panjang vektor, dan Cosine Similarity secara manual tanpa library numerik?
3. Bagaimana membandingkan kasus baru dengan seluruh kasus lama serta menentukan kasus yang paling mirip?
4. Bagaimana menyajikan hasil perhitungan tersebut melalui antarmuka web dinamis?
5. Bagaimana membuktikan bahwa perhitungan inti tidak diambil alih oleh library tertentu?

### 1.3 Tujuan

Tujuan proyek ini adalah:

1. Membangun aplikasi Streamlit yang dapat menerima data pasien dan pilihan gejala.
2. Mengimplementasikan perhitungan CBR dan Cosine Similarity secara manual di Python murni.
3. Menghasilkan peringkat kemiripan dan kasus rujukan paling mirip.
4. Menguji implementasi dengan unit test agar hasilnya sesuai kode acuan.
5. Menyusun laporan yang menjelaskan alur logika, rumus, dan hasil perhitungan secara transparan.

### 1.4 Manfaat

Manfaat proyek ini antara lain:

- **Bagi Penulis**, memperdalam pemahaman tentang CBR, Cosine Similarity, dan implementasi algoritma tanpa bergantung pada library otomatis.
- **Bagi dosen**, menyediakan kode yang dapat diaudit baris per baris.
- **Bagi pengguna**, memberikan rekomendasi awal berdasarkan kemiripan gejala, dengan catatan bahwa hasil bukan diagnosis final.

### 1.5 Ruang Lingkup

Ruang lingkup proyek ini meliputi:

- Dua dataset: DHF (14 atribut biner, 4 kasus) dan P006 (19 atribut berbobot, 5 kasus).
- Proses input berupa data diri dan pilihan gejala; data diri tidak ikut dihitung.
- Perhitungan kemiripan memakai Cosine Similarity manual.
- Antarmuka berbasis Streamlit dengan alur: beranda → identitas → gejala → hasil.
- Database **belum** diintegrasikan; data saat ini masih tersimpan sebagai konstanta di `data/dataset.py`. Integrasi database dibahas sebagai rekomendasi pada bagian Penutup.

---

## Isi

### 2.1 Landasan Teori

#### 2.1.1 Sistem Pendukung Keputusan

Sistem Pendukung Keputusan adalah sistem berbasis komputer yang membantu pengambilan keputusan dengan mengolah data dan menghasilkan informasi yang relevan. Dalam proyek ini, keputusan yang dibantu adalah menentukan grade DHF yang paling mirip dengan pola gejala pasien.

#### 2.1.2 Case-Based Reasoning

Case-Based Reasoning bekerja dengan prinsip bahwa masalah baru dapat diselesaikan dengan melihat penyelesaian masalah lama yang serupa. Secara konseptual, CBR memiliki empat siklus:

| Siklus | Penjelasan | Status di proyek |
|---|---|---|
| *Retrieve* | Mengambil kasus lama yang paling mirip | Sudah diimplementasikan |
| *Reuse* | Memakai solusi kasus tersebut sebagai rekomendasi | Sudah diimplementasikan |
| *Revise* | Menyesuaikan solusi jika diperlukan | Belum diimplementasikan |
| *Retain* | Menyimpan pengalaman baru ke basis kasus | Belum diimplementasikan |

Dua siklus pertama menjadi fokus project ini, sesuai batasan ruang lingkup.

#### 2.1.3 Cosine Similarity

Cosine Similarity mengukur kesamaan dua vektor melalui cosinus sudut di antaranya. Rumus yang dipakai:

```text
dot(A, B)   = Σ (A[j] × B[j])
ΣA²         = Σ (A[j]²)
ΣB²         = Σ (B[j]²)
|A|         = √(ΣA²)
|B|         = √(ΣB²)
Cosine(A,B) = dot(A, B) / (|A| × |B|)
Persentase  = Cosine × 100%
```

Jika `|A| × |B| = 0`, maka nilai cosine ditetapkan `0.0` agar tidak terjadi pembagian dengan nol.

Untuk vektor dengan nilai non-negatif seperti gejala (0/1 atau 0/1/3/5), nilai cosine berada pada rentang 0 sampai 1. Nilai mendekati 1 berarti pola kedua vektor semakin mirip.

#### 2.1.4 Studi Terkait

Jatmiko, Junaedi, dan Imrona (2017) meneliti sistem pakar untuk diagnosis demam berdarah dengan menggabungkan CBR, Rule-Based Reasoning, dan probabilitas Bayes. Penelitian mereka melaporkan tingkat akurasi 92%. Angka tersebut merupakan hasil penelitian mereka, **bukan** akurasi aplikasi CekDBD yang dibangun dalam proyek ini.

### 2.2 Analisis dan Desain Sistem

#### 2.2.1 Kebutuhan Sistem

Kebutuhan fungsional:

1. Pengguna dapat mengisi nama, usia, dan jenis kelamin.
2. Pengguna dapat memilih satu atau lebih gejala.
3. Sistem membentuk vektor kasus baru dari gejala yang dipilih.
4. Sistem menghitung kemiripan dengan setiap kasus lama.
5. Sistem menampilkan kasus paling mirip dan peringkat seluruh kasus.
6. Pengguna dapat melihat matriks dataset.

Kebutuhan nonfungsional:

1. Perhitungan inti ditulis manual dengan Python dasar.
2. Tidak memakai NumPy, Pandas, scikit-learn, atau library numerik lain.
3. Kode mudah dibaca dan diaudit.
4. Pembulatan angka hanya dilakukan saat tampil, bukan sebelum perankingan.

#### 2.2.2 Alur Data

```text
Input gejala (checkbox)
        │
        ▼
buat_kasus_baru() → vektor [0/1, ...]
        │
        ▼
validasi_vektor() → panjang & tipe nilai dicek
        │
        ▼
hitung_cbr() ──► hitung_detail() ──► cosine_similarity()
        │                                  │
        │                                  ├─ dot
        │                                  ├─ ΣA², ΣB²
        │                                  ├─ |A|, |B|
        │                                  └─ cosine
        ▼
urutkan_hasil() + kasus_terbaik()
        │
        ▼
result_view.py → laporan & grafik
```

#### 2.2.3 Struktur Modul

| Modul | Tanggung jawab |
|---|---|
| `app.py` | Entry point dan navigasi halaman |
| `core/cosine_similarity.py` | Rumus manual dot product, kuadrat, akar, cosine |
| `core/cbr.py` | Pembentukan vektor, perbandingan kasus, ranking, kasus terbaik |
| `data/dataset.py` | Dataset DHF dan P006 |
| `utils/validation.py` | Validasi vektor, pasien, dan pilihan gejala |
| `components/` | Tampilan dan interaksi Streamlit |
| `tests/` | Pengujian unit dengan `unittest` |

#### 2.2.4 Desain Vektor Kasus

| Dataset | Atribut | Kasus lama | Nilai |
|---|---:|---:|---|
| DHF | G1–G14 (14) | DHF1–DHF4 | 0 / 1 |
| P006 | F1–F19 (19) | P001–P005 | 0/1/3/5 pada kasus lama; 0/1 pada contoh kasus baru |

Contoh kasus baru DHF:

```text
[1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]
```

Contoh kasus baru P006:

```text
[0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
```

#### 2.2.5 Rancangan Integrasi Database (Rencana)

Pada kondisi saat ini, data masih berupa konstanta Python. Rencana pengembangannya adalah menambahkan lapisan repository dengan `sqlite3` dari standard library atau OpenPyXL hanya untuk membaca Excel. Data yang dibaca diubah menjadi `dict` sederhana:

```python
{
    "kode": "DHF2",
    "nama": "Demam Berdarah Grade II",
    "vektor": [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
}
```

Selanjutnya data tersebut dikirim ke `core/cbr.py`. Perhitungan cosine tetap berada di Python, tidak dipindahkan ke query SQL maupun rumus Excel.

### 2.3 Implementasi Perhitungan Manual

#### 2.3.1 Pembentukan Vektor Kasus Baru

Fungsi `buat_kasus_baru()` mengubah daftar kode gejala yang dipilih menjadi vektor biner:

```python
def buat_kasus_baru(terpilih, atribut):
    kasusbaru = []
    for a in atribut:
        kasusbaru.append(1 if a["kode"] in terpilih else 0)
    return kasusbaru
```

Nilai `1` berarti gejala dipilih, nilai `0` berarti tidak dipilih.

#### 2.3.2 Dot Product, Kuadrat, dan Panjang Vektor

Berikut potongan `core/cosine_similarity.py`:

```python
dot = 0
kuadrat_kasusbaru = 0
kuadrat_kasus = 0

for j in range(len(kasusbaru)):
    dot += kasusbaru[j] * kasus[j]
    kuadrat_kasusbaru += kasusbaru[j] ** 2
    kuadrat_kasus += kasus[j] ** 2

panjang_kasusbaru = kuadrat_kasusbaru ** 0.5
panjang_kasus = kuadrat_kasus ** 0.5
```

Penjelasan:

- `dot` menampung hasil perkalian elemen yang sepadan.
- `kuadrat_kasusbaru` dan `kuadrat_kasus` menampung jumlah kuadrat masing-masing vektor.
- `** 0.5` adalah pangkat satu per dua, digunakan sebagai akar kuadrat manual.

#### 2.3.3 Cosine Similarity

```python
if panjang_kasusbaru * panjang_kasus == 0:
    cosine = 0.0
else:
    cosine = dot / (panjang_kasusbaru * panjang_kasus)
```

Kondisi nol menangani kasus ketika salah satu vektor seluruhnya bernilai nol. Hal ini sesuai dengan kode acuan yang diberikan Penulis.

#### 2.3.4 Perbandingan Kasus dan Penentuan Terbaik

```python
def hitung_cbr(kasusbaru, kasus_lama):
    hasil = []
    for kasus in kasus_lama:
        detail = hitung_detail(kasusbaru, kasus["vektor"])
        hasil.append({
            "kode": kasus["kode"],
            "nama": kasus["nama"],
            "dot": detail["dot"],
            "cosine": detail["cosine"],
            "persentase": detail["cosine"] * 100,
        })
    return hasil


def kasus_terbaik(hasil):
    if not hasil:
        return None
    terbaik = hasil[0]
    for item in hasil[1:]:
        if item["cosine"] > terbaik["cosine"]:
            terbaik = item
    return terbaik
```

`kasus_terbaik()` memakai perulangan dan operator perbandingan `>` secara eksplisit. Pendekatan ini lebih rinci daripada kode acuan yang memakai `max()` dan `.index()`, tetapi menghasilkan nilai yang sama.

Untuk keperluan tampilan, `urutkan_hasil()` memakai fungsi bawaan Python:

```python
return sorted(hasil, key=lambda item: item["cosine"], reverse=True)
```

Fungsi ini hanya mengurutkan nilai cosine yang sudah dihitung manual; ia tidak menghitung cosine.

#### 2.3.5 Detail Perhitungan

Fungsi `hitung_detail()` mengembalikan komponen perhitungan seperti `dot`, `kuadrat_kasusbaru`, `kuadrat_kasus`, `panjang_kasusbaru`, `panjang_kasus`, `penyebut`, dan `cosine`. Komponen ini berguna untuk keperluan audit, meskipun saat ini belum ditampilkan seluruhnya di antarmuka.

### 2.4 Hasil Pengujian dan Pembahasan

#### 2.4.1 Lingkungan Pengujian

Pengujian dijalankan dengan perintah:

```bash
python -m unittest discover -s tests -v
```

Hasil: **10 test lulus (OK)**.

#### 2.4.2 Hasil Dataset DHF

| Kasus | Dot | Cosine | Persentase |
|---|---:|---:|---:|
| DHF1 | 5 | 0.7905694150 | 79,06% |
| DHF2 | 6 | 0.8660254038 | 86,60% |
| DHF3 | 6 | 0.8017837257 | 80,18% |
| DHF4 | 4 | 0.5773502692 | 57,74% |

Kasus paling mirip: **DHF2 — Demam Berdarah Grade II**.

#### 2.4.3 Hasil Dataset P006

| Kasus | Dot | Cosine | Persentase |
|---|---:|---:|---:|
| P001 | 2 | 0.1145196669 | 11,45% |
| P002 | 0 | 0.0000000000 | 0,00% |
| P003 | 4 | 0.2236067977 | 22,36% |
| P004 | 16 | 0.8207826817 | 82,08% |
| P005 | 0 | 0.0000000000 | 0,00% |

Kasus paling mirip: **P004 — Tumor Lambung**.

#### 2.4.4 Contoh Penelusuran Angka

**DHF vs DHF2**

```text
dot        = 6
ΣA²        = 8   → |A| ≈ 2.8284
ΣB²        = 6   → |B| ≈ 2.4495
cosine     = 6 / (2.8284 × 2.4495) = 0.8660
persentase = 86,60%
```

**P006 vs P004**

```text
dot        = 16
ΣA²        = 5   → |A| ≈ 2.2361
ΣB²        = 76  → |B| ≈ 8.7178
cosine     = 16 / (2.2361 × 8.7178) = 0.8208
persentase = 82,08%
```

#### 2.4.5 Audit Kesesuaian dengan Kode Acuan

| No | Aspek yang diperiksa | Hasil |
|---|---|---|
| 1 | Dot product dihitung manual dengan perulangan dan perkalian | Sesuai |
| 2 | Panjang vektor memakai penjumlahan kuadrat dan akar manual | Sesuai |
| 3 | Cosine dihitung dengan operasi matematika dasar | Sesuai |
| 4 | Perbandingan kasus dan kasus terbaik memakai logika dasar Python | Sesuai |
| 5 | Ada library yang mengambil alih perhitungan | Tidak ada |

Fungsi bawaan yang muncul, yaitu `sorted()`, `sum()`, `max()`, dan `min()`, hanya dipakai untuk pengurutan, rekap tampilan, dan pembatasan tinggi grafik. Tidak ada fungsi tersebut yang menghitung dot product maupun cosine.

#### 2.4.6 Temuan dan Batasan

1. **Database belum tersedia.** Data masih hard-code di `data/dataset.py`. Ini bukan kesalahan perhitungan, melainkan belum terpenuhinya target integrasi database.
2. **Duplikasi perhitungan.** `hitung_detail()` menghitung ulang kuadrat yang sudah dihitung `cosine_similarity()`. Hasil saat ini konsisten, tetapi berisiko jika salah satu bagian diubah.
3. **Pengurutan memakai `sorted()`.** Masih dalam kategori built-in Python, bukan library perhitungan. Dapat diganti sorting manual jika diperlukan untuk keperluan akademik.
4. **Detail belum tampil di UI.** Komponen perhitungan sudah tersedia dari `hitung_detail()`, tetapi belum ditampilkan di halaman hasil.

### 2.5 Tampilan Aplikasi

Aplikasi memiliki lima alur tampilan:

1. **Beranda** — penjelasan singkat CBR dan metode.
2. **Data diri** — nama, usia, jenis kelamin; hanya untuk laporan.
3. **Pilih gejala** — 14 checkbox gejala DHF.
4. **Hasil** — grade paling mirip, persentase, dan grafik perbandingan.
5. **Dataset** — matriks gejala terhadap kasus rujukan.

Identitas pasien sengaja tidak dimasukkan ke dalam vektor agar tidak memengaruhi perhitungan kemiripan.

---

## Penutup

### 3.1 Kesimpulan

Berdasarkan analisis, implementasi, dan pengujian yang telah dilakukan, beberapa kesimpulan dapat ditarik:

1. Aplikasi CekDBD berhasil dibangun dengan Streamlit dan dapat menerima input gejala DHF.
2. Seluruh perhitungan inti CBR dan Cosine Similarity ditulis manual dengan perulangan dan operasi matematika dasar Python.
3. Tidak ditemukan penggunaan NumPy, Pandas, scikit-learn, atau library numerik lain pada jalur perhitungan.
4. Hasil pengujian dengan 10 unit test menunjukkan implementasi sesuai kode acuan, baik untuk dataset DHF maupun P006.
5. Kasus paling mirip berturut-turut adalah DHF2 untuk dataset DHF dan P004 untuk dataset P006.
6. Integrasi database dan tampilan detail perhitungan masih menjadi pengembangan lanjutan.

### 3.2 Rekomendasi

Beberapa saran untuk pengembangan selanjutnya:

1. Menambahkan lapisan repository berbasis `sqlite3` atau OpenPyXL hanya untuk membaca data, lalu mengonversinya menjadi `dict` Python sebelum masuk ke `core/`.
2. Menyatukan perhitungan di `hitung_detail()` agar hanya ada satu sumber angka untuk dot product dan cosine.
3. Mengganti `sorted()` dengan bubble sort atau insertion sort manual apabila diperlukan agar seluruh proses benar-benar tertulis baris per baris.
4. Menambahkan expander “Lihat perhitungan CBR” pada halaman hasil agar komponen dot product, akar, dan cosine dapat ditunjukkan langsung kepada pemeriksa.
5. Mengimplementasikan siklus *Revise* dan *Retain* pada CBR agar sistem dapat menyimpan kasus baru sebagai pengetahuan tambahan.

### 3.3 Penutup

Proyek ini membuktikan bahwa perhitungan CBR dan Cosine Similarity dapat diimplementasikan tanpa bergantung pada library otomatis. Dengan memahami setiap tahap perhitungan mulai dari dot product, panjang vektor, hingga penentuan kasus terbaik, Penulis dapat menjelaskan dan mempertanggungjawabkan logika sistem secara menyeluruh. Hasil kemiripan yang ditampilkan tetap merupakan rekomendasi awal dan perlu dikonfirmasi oleh tenaga medis.

---

## Daftar Pustaka

1. Jatmiko, A. D., Junaedi, D., & Imrona, M. (2017). Analisis dan Implementasi Sistem Pakar dengan Metode Case Based Reasoning dan Rule Based Reasoning (Studi Kasus: Diagnosis Penyakit Demam Berdarah). *e-Proceeding of Engineering*, 4(2), 3269–3276. Universitas Telkom.
2. Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org/3/
3. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/

---

## Lampiran Singkat

### Lampiran A — Daftar File Penting

```text
app.py
core/cosine_similarity.py
core/cbr.py
data/dataset.py
utils/validation.py
components/input_form.py
components/result_view.py
tests/test_cosine_similarity.py
docs/AUDIT_CBR_IMPLEMENTASI.md
docs/KODE_DASAR_CBR_PENGGUNA.md
PROMPT_LAPORAN_AKHIR.md
Konteks-Proyek-SPK-CBR.zip
```

### Lampiran B — Kode Acuan

Kode dasar Cosine Similarity yang diberikan Penulis tersimpan lengkap di:

```text
docs/KODE_DASAR_CBR_PENGGUNA.md
```

### Lampiran C — Perintah Verifikasi

```bash
python -m unittest discover -s tests -v
```
