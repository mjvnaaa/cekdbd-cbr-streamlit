# Perbandingan Implementasi JavaScript dan Python

| Aspek | JavaScript lama | Python (Streamlit) |
|---|---|---|
| Bahasa perhitungan | `js/cbr.js` | `core/cosine_similarity.py`, `core/cbr.py` |
| Rumus cosine | Dot product / (panjang K1 × panjang kasus) | Sama persis |
| Cara hitung | Perulangan `for` manual | Perulangan `for` manual |
| Library numerik | Tidak ada | Tidak ada |
| Dataset DHF | `js/data.js` | `data/dataset.py` (disalin apa adanya) |
| Dataset P006 | Tidak ada | `data/dataset.py` (dari kode pengguna) |
| Nama gejala DHF | G1–G14 dengan nama asli | Sama |
| Nama atribut P006 | Tidak tersedia | F1–F19, tanpa nama rekaan |
| Pembagian dengan nol | Tidak ditangani (bisa `NaN`) | Ditangani: `cosine = 0.0` |
| Ranking | Bubble sort pada salinan array | `sorted(..., reverse=True)` stabil |
| Kasus terbaik | Posisi nilai cosine maksimum | `kasus_terbaik()` dengan perbandingan manual |
| Pembulatan | `.toFixed()` saat tampil | `f"{x:.4f}"` saat tampil; ranking memakai nilai penuh |
| Navigasi | Hash URL (`#/identitas` → `#/gejala` → `#/hasil`) | Alur 3 langkah: data diri → gejala → hasil |
| Penyimpanan state | `sessionStorage` | `st.session_state` |
| Identitas pasien | Ada, tidak dihitung | Ada di form data diri, tidak dihitung, hanya ditampilkan di laporan hasil |
| Tampilan | HTML + CSS + ikon Lucide | Streamlit + CSS tema warna lama |

## Kesetaraan hasil

Dengan kasus baru DHF `[1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]`, kedua
implementasi menghasilkan dot product `[5, 6, 6, 4]` dan cosine
`[0.7906, 0.8660, 0.8018, 0.5774]`. Kasus terbaik: **DHF2**.

Dengan kasus baru P006 yang diberikan pengguna, dot product
`[2, 0, 4, 16, 0]` dan cosine
`[0.1145, 0.0000, 0.2236, 0.8208, 0.0000]`. Kasus terbaik: **P004 — Tumor Lambung**.

## Perbedaan yang disengaja

1. **Penanganan nol.** Kode Python pengguna secara eksplisit menetapkan
   `cosine = 0.0` bila `panjang_kasusbaru * panjang_kasus == 0`. Aturan ini
   dipertahankan pada migrasi meskipun JS lama belum memilikinya.
2. **P006 ditambahkan.** Logika P006 berasal dari kode Python yang Anda kirim,
   bukan dari file JavaScript lama. Karena itu tidak ada padanan file JS untuk
   dataset ini.
3. **Nama atribut P006.** Tidak dibuat nama gejala baru; kode `F1`–`F19`
   digunakan sebagai label netral dan dijelaskan pada dokumentasi.
4. **Metode pengurutan.** Penggantian bubble sort dengan `sorted` tidak mengubah
   hasil karena keduanya mengurutkan nilai cosine yang sama dan `sorted` stabil
   untuk nilai kemiripan yang identik.
5. **Antarmuka dipangkas untuk pengguna umum.** Proyek lama memiliki lima halaman
   termasuk laporan lengkap dan dataset. Streamlit kini memakai alur tiga langkah
   yang sama dengan alur inti JS (data diri → gejala → hasil). Identitas pasien
   tetap diminta seperti proyek lama, tetapi hanya dipakai sebagai kop laporan.
   Halaman teknis (dataset, detail vektor, perbandingan P006) tidak dijadikan
   menu utama agar pengguna tidak dibingungkan; detail matematis masih bisa dibuka
   dari hasil bila diperlukan untuk keperluan akademik.

## Verifikasi

Jalankan:

```bash
python -m unittest discover -s tests -v
```

Semua nilai acuan pada pengujian berasal dari perhitungan manual dengan logika
yang sama seperti kode yang Anda kirim.
