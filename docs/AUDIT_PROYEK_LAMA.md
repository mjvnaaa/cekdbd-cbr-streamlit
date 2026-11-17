# Audit Proyek Lama

Audit dilakukan terhadap seluruh direktori proyek sebelum migrasi. Proyek lama
tidak diubah.

## Struktur yang ditemukan

```text
Tugas Akhir/
├── index.html
├── css/style.css
├── js/data.js
├── js/cbr.js
├── js/app.js
├── .github/workflows/static.yml
└── PROMPT_MIGRASI_SPK_STREAMLIT.md
```

Direktori `.git/` berisi metadata repositori dan bukan merupakan kode aplikasi.

## Daftar file yang diperiksa

| File | Fungsi |
|---|---|
| `index.html` | Struktur halaman, navbar, footer, tempat `.nav`, `#app`, dan pemuatan tiga file JavaScript. Judul lama: **CekDBD - Cek Grade Demam Berdarah**. |
| `css/style.css` | Palet warna dan gaya visual: `#03045E`, `#0077B6`, `#00B4D8`, `#90E0EF`, `#CAF0F8`, latar `#F3FBFD`, teks `#0E1A3D`, font Inter. Komponen: navbar pil, tombol pil, kartu, stepper, tabel, chart batang, sheet laporan. |
| `js/data.js` | `GEJALA` berisi 14 gejala (G1–G14) dengan nama asli; `KASUS_LAMA` berisi 4 kasus DHF1–DHF4 dengan vektor biner 14 elemen. |
| `js/cbr.js` | `buatKasusBaru(terpilih)` mengubah gejala terpilih menjadi vektor 0/1; `hitungCBR(K1)` menghitung dot product, jumlah kuadrat, panjang vektor, cosine, lalu mencari nilai tertinggi dan mengurutkan dengan bubble sort. |
| `js/app.js` | Router berbasis hash: `/`, `/identitas`, `/gejala`, `/hasil`, `/dataset`. Menyimpan identitas pasien dan gejala terpilih di `sessionStorage`. Identitas tidak ikut dihitung. |
| `.github/workflows/static.yml` | Workflow GitHub Pages untuk Deploy static content dari akar repositori. |
| `PROMPT_MIGRASI_SPK_STREAMLIT.md` | Spesifikasi migrasi, struktur target, ketentuan logika, UI/UX, dokumentasi, identitas akademik, dan referensi. |

## Fitur yang ditemukan pada aplikasi lama

1. Beranda dengan penjelasan singkat CBR dan visualisasi pola gejala.
2. Form identitas pasien (nama, usia, jenis kelamin) sebagai pelengkap laporan.
3. Pemilihan 14 gejala: 11 keluhan dan 3 hasil lab darah (G12–G14).
4. Laporan hasil: grade paling mirip, tingkat kemiripan, perbandingan tiap grade,
   daftar gejala terpilih, serta detail perhitungan yang bisa dibuka.
5. Halaman dataset dengan pencarian gejala dan matriks keberadaan gejala per grade.

## Dataset yang ditemukan

- **DHF**: 14 atribut biner dan 4 kasus lama. Sumber data: Jatmiko, Junaedi, dan
  Imrona (2017), Tabel 2-1 sampai 2-3 (dicantumkan di `js/data.js` dan footer `index.html`).
- **P006**: tidak ada di proyek JavaScript. Dataset ini berasal dari contoh kode
  Python yang diberikan pengguna: 19 atribut, 5 kasus lama (P001–P005), bobot
  0/1/3/5 pada kasus lama dan 0/1 pada kasus baru contoh.

## Metode dan rumus

JS dan Python yang diberikan memakai Cosine Similarity manual:

```text
dot = Σ(ai × bi)
kuadrat_a = Σ(ai²)
kuadrat_b = Σ(bi²)
cosine = dot / (√kuadrat_a × √kuadrat_b)
persentase = cosine × 100%
```

## Komponen desain yang dijadikan referensi

- Warna utama biru tua (`#03045E`) dengan aksen biru cerah dan turquoise.
- Latar terang (`#F3FBFD`) dan kartu putih berborder biru muda.
- Navbar berbentuk pil dan tombol berbentuk pil.
- Stepper tiga langkah pada proses diagnosis.
- Tabel detail perhitungan dan chart perbandingan persentase.

Warna tersebut dipindahkan ke `.streamlit/config.toml` dan CSS di `app.py`.

## Perbedaan dan masalah yang ditemukan

1. `js/cbr.js` tidak menangani pembagian dengan nol. Jika vektor kasus baru semua
   nol, hasil cosine menjadi `NaN`. Kode Python yang diberikan pengguna sudah
   menangani kasus ini dengan `cosine = 0.0`; implementasi migrasi memakai aturan Python.
2. JS hanya menyediakan dataset DHF. Logika P006 belum ada di proyek lama dan
   ditambahkan di versi Streamlit sesuai permintaan.
3. Kode P006 yang diberikan tidak mencantumkan nama atribut, sehingga migrasi
   memakai kode `F1`–`F19` tanpa mengarang nama gejala.
4. JS mengurutkan dengan bubble sort; Python memakai `sorted` yang stabil. Untuk
   data saat ini, urutan ranking yang dihasilkan tetap sama.
5. Identitas pasien di JS hanya untuk laporan dan tidak memengaruhi perhitungan.
   Pada Streamlit, input yang dihitung hanya nilai atribut kasus baru.

## Rekomendasi migrasi yang dilakukan

- Memisahkan perhitungan (`core/`), dataset (`data/`), tampilan (`components/`),
  validasi (`utils/`), pengujian (`tests/`), dan dokumentasi (`docs/`).
- Mempertahankan rumus dan nilai dataset secara eksak.
- Menambahkan penanganan pembagian dengan nol sesuai kode Python pengguna.
- Membuat alur tiga langkah (data diri → gejala → hasil) dengan tema warna lama,
  menyesuaikan kebutuhan pengguna umum.
- Menuliskan hasil perhitungan aktual pada dokumentasi agar dapat ditelusuri.
