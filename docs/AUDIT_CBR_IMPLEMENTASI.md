# Audit Implementasi CBR & Cosine Similarity

**Tanggal:** 21 November 2026  
**Objek:** Project `Tugas-Akhir-Streamlit` — CekDBD  
**Status:** Audit saja. Tidak ada perubahan pada logika perhitungan. Working tree bersih sebelum penambahan berkas konteks.

---

## 1. Kesimpulan

Perhitungan inti Case-Based Reasoning dan Cosine Similarity sudah diimplementasikan secara manual menggunakan perulangan dan operasi matematika dasar Python. Tidak ditemukan penggunaan NumPy, Pandas, scikit-learn, SciPy, atau library numerik/ML lain pada jalur perhitungan.

Yang belum sesuai dengan target pengembangan: integrasi database belum tersedia, data masih berupa konstanta di `data/dataset.py`. Ini bukan pelanggaran terhadap rumus CBR, melainkan gap terhadap kebutuhan web dinamis + database.

---

## 2. Jawaban atas lima pertanyaan audit

| No | Pertanyaan | Verdict | Bukti |
|---|---|---|---|
| 1 | Dot product dihitung manual dengan perulangan dan operasi perkalian? | Ya | `core/cosine_similarity.py`: `for j in range(len(kasusbaru)): dot += kasusbaru[j] * kasus[j]` |
| 2 | Panjang vektor memakai penjumlahan kuadrat dan akar secara manual? | Ya | Akumulasi `nilai ** 2` di loop yang sama, lalu `kuadrat ** 0.5` |
| 3 | Cosine dihitung dengan operasi matematika dasar? | Ya | `cosine = dot / (panjang_kasusbaru * panjang_kasus)`; nol ditangani dengan `0.0` |
| 4 | Perbandingan tiap kasus dan penentuan tertinggi memakai logika dasar Python? | Ya | `hitung_cbr()` memakai `for`; `kasus_terbaik()` memakai perbandingan `>` manual. Ranking memakai `sorted()` bawaan Python. |
| 5 | Ada library/fungsi yang mengambil alih perhitungan? | Tidak untuk rumus | `sorted()` hanya ranking; `sum()` di `info_view.py` hanya footer tabel; `max()/min()` di `result_view.py` hanya membatasi tinggi batang grafik. |

---

## 3. Verifikasi numerik

Perintah:

```bash
python -m unittest discover -s tests -v
```

Hasil: **Ran 10 tests — OK**.

| Dataset | Dot product | Cosine | Kasus terbaik |
|---|---|---|---|
| DHF | `[5, 6, 6, 4]` | `[0.7905694150, 0.8660254038, 0.8017837257, 0.5773502692]` | DHF2 |
| P006 | `[2, 0, 4, 16, 0]` | `[0.1145196669, 0.0, 0.2236067977, 0.8207826817, 0.0]` | P004 |

Contoh penelusuran:

```text
P006 vs P004:
dot = 16
ΣA² = 5   -> |A| = 2.2361
ΣB² = 76  -> |B| = 8.7178
cosine = 16 / (2.2361 × 8.7178) = 0.8208 -> 82,08%
```

---

## 4. Temuan dan rekomendasi

### 4.1 Database belum diimplementasikan

Saat ini dataset didefinisikan di `data/dataset.py` dan `app.py` mengimpor `DHF` secara langsung. Fungsi `get_dataset(key)` tersedia tetapi belum dipakai untuk pemilihan dinamis. `requirements.txt` hanya berisi `streamlit>=1.39.0`.

Rekomendasi: tambahkan lapisan repository memakai `sqlite3` (standard library) atau OpenPyXL hanya untuk membaca data. Konversi baris menjadi `dict` dengan kunci `kode`, `nama`, `vektor`, lalu serahkan ke `core/cbr.py`. Jangan memindahkan perhitungan cosine ke SQL atau Excel.

### 4.2 Duplikasi perhitungan di `hitung_detail()`

`cosine_similarity()` sudah menghitung kuadrat, tetapi `hitung_detail()` menghitung ulang kuadrat pada loop kedua. Angka saat ini konsisten (diuji oleh `test_detail_konsisten_dengan_fungsi_utama`), namun berisiko jika salah satu bagian diubah di kemudian hari.

Rekomendasi: jadikan satu fungsi sebagai sumber tunggal komponen perhitungan, lalu `cosine_similarity()` mengambil `dot` dan `cosine` dari hasil tersebut. Rumus tidak berubah.

### 4.3 Penggunaan `sorted()`

`urutkan_hasil()` memakai `sorted(..., reverse=True)`. Ini adalah fungsi bawaan Python, bukan library perhitungan, dan tidak mengubah nilai cosine. Jika dosen menginginkan pengurutan ditulis manual, dapat diganti bubble sort atau insertion sort; update dokumentasi dan test bila dilakukan.

### 4.4 Detail perhitungan belum tampil di antarmuka

`hitung_detail()` sudah mengembalikan `dot`, `kuadrat_kasusbaru`, `kuadrat_kasus`, `panjang_kasusbaru`, `panjang_kasus`, `penyebut`, dan `cosine`, tetapi `components/result_view.py` saat ini hanya menampilkan persentase dan grafik.

Rekomendasi: tambahkan expander "Lihat perhitungan CBR" pada halaman hasil agar proses dapat ditunjukkan langsung saat pertanggungjawaban laporan.

---

## 5. Hubungan dengan laporan akhir

Ringkasan ini dipakai oleh `PROMPT_LAPORAN_AKHIR.md` pada bagian Bab IV, sub-bab "Audit Kesesuaian dengan Kode Acuan", dan Bab V, sub-bab "Rekomendasi".

Kode acuan asli dari Penulis tersimpan di `docs/KODE_DASAR_CBR_PENGGUNA.md`.
