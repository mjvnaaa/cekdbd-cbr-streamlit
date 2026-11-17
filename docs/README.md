# SPK Kemiripan Kasus — CBR + Cosine Similarity (Streamlit)

Versi Python dari proyek SPK sebelumnya. Seluruh perhitungan dijalankan oleh Python
bawaan; Streamlit hanya menjadi antarmuka. Proyek HTML/CSS/JavaScript lama tidak
diubah atau dihapus.

## Menjalankan aplikasi

```bash
cd Tugas-Akhir-Streamlit
pip install -r requirements.txt
streamlit run app.py
```

Buka alamat yang ditampilkan Streamlit (biasanya `http://localhost:8501`).

## Deploy ke Streamlit Community Cloud (gratis)

1. Buat repository baru di GitHub, lalu upload seluruh isi folder
   `Tugas-Akhir-Streamlit` (file `.gitignore` sudah menyisihkan `venv/`).
   Dari PowerShell di folder proyek:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<username>/<nama-repo>.git
   git branch -M main
   git push -u origin main
   ```

2. Buka <https://share.streamlit.io>, login dengan GitHub, lalu pilih
   **New app**.
3. Isi: repository = repo di atas, branch = `main`,
   **Main file path = `app.py`**.
4. Klik **Deploy**. Setelah selesai, alamat `https://<nama-app>.streamlit.app`
   bisa dibagikan (misalnya ke dosen).

Catatan: `requirements.txt` sudah berisi `streamlit>=1.39.0` dan tidak ada
rahasia/API key, jadi tidak perlu menambahkan *secrets*. Jangan meng-upload
folder `venv/` karena ukurannya besar dan tidak dipakai di server.

## Struktur folder

```text
Tugas-Akhir-Streamlit/
├── app.py                         # entry point Streamlit + navigasi
├── core/
│   ├── cosine_similarity.py       # rumus manual + detail perhitungan
│   └── cbr.py                     # pembandingan, ranking, kasus terbaik
├── data/
│   └── dataset.py                 # dataset DHF dan P006
├── components/
│   ├── dashboard.py               # halaman awal yang ramah pengguna
│   ├── input_form.py              # data diri + pilih gejala
│   ├── result_view.py             # hasil sederhana (tanpa detail perhitungan)
│   └── info_view.py               # arsip halaman informasi (tidak dipakai di alur umum)
├── utils/
│   └── validation.py              # validasi panjang dan tipe nilai vektor
├── tests/
│   └── test_cosine_similarity.py  # pengujian dengan unittest
├── docs/
│   ├── README.md
│   ├── AUDIT_PROYEK_LAMA.md
│   ├── DOKUMENTASI_PERHITUNGAN.md
│   └── PERBANDINGAN_JS_PYTHON.md
├── .streamlit/config.toml         # tema warna mengikuti desain lama
└── requirements.txt
```

## Dataset

| Dataset | Jumlah atribut | Kasus lama | Nilai | Sumber |
|---|---:|---:|---|---|
| DHF | 14 | 4 (DHF1–DHF4) | 0 / 1 | `js/data.js`, Jatmiko dkk. (2017) |
| P006 | 19 | 5 (P001–P005) | 0 / 1 / 3 / 5 | Kode Python yang diberikan pengguna |

Nama atribut DHF memakai nama gejala asli dari `js/data.js`. Dataset P006 tidak
memiliki daftar nama atribut di kode sumber, sehingga atributnya diberi kode
`F1` sampai `F19`; tidak ada nama gejala yang dikarang.

Antarmuka pengguna umum sengaja difokuskan pada **DHF** karena gejalanya punya
nama yang jelas dan bisa dicentang. Dataset P006 tetap tersimpan di `data/`,
`core/`, dan `tests/`, tetapi tidak ditampilkan di alur aplikasi agar pengguna
tidak dibingungkan dengan kode `F1`–`F19` dan bobot `0/1/3/5`.

## Alur pengguna

1. **Mulai** — penjelasan singkat dan tombol mulai pemeriksaan.
2. **Data diri** — nama, usia, dan jenis kelamin. Identitas hanya untuk laporan.
3. **Pilih gejala** — centang keluhan dan hasil pemeriksaan darah yang dialami.
4. **Hasil** — penyakit/grade paling mirip ditampilkan dengan persentase kemiripan
   dan grafik perbandingan tiap grade. Detail perhitungan CBR tidak ditampilkan
   kepada pengguna.

## Pengujian

```bash
python -m unittest discover -s tests -v
```

Pengujian mencakup hasil DHF dan P006, penanganan vektor nol, validasi jumlah
atribut, konsistensi detail perhitungan, dan pembentukan vektor gejala DHF.

## Identitas & referensi

| Informasi | Keterangan |
|---|---|
| Nama | Moh. Jevon Attaillah |
| NIM | 362458302035 |
| Kelas | TRPL 3D |
| Program studi | Rekayasa Perangkat Lunak |
| Mata kuliah | Sistem Pendukung Keputusan (SPK) |
| Judul aplikasi | CekDBD — Sistem Pendukung Keputusan Kemiripan Kasus Menggunakan CBR dan Cosine Similarity |

Identitas ini ditampilkan secara ringkas di sidebar dan bisa dilihat lengkap
pada expander **Identitas aplikasi & referensi** di halaman awal aplikasi.

```bibtex
@article{Jatmiko2017,
  author    = {Jatmiko, Arman Dwi and Junaedi, Danang and Imrona, Mahmud},
  title     = {Analisis Dan Implementasi Sistem Pakar Dengan Metode Case Based Reasoning Dan Rule Based Reasoning (Studi Kasus: Diagnosis Penyakit Demam Berdarah)},
  journal   = {e-Proceeding of Engineering},
  year      = {2017},
  month     = aug,
  volume    = {4},
  number    = {2},
  pages     = {3269--3276},
  issn      = {2355-9365},
  publisher = {Universitas Telkom},
  keywords  = {case based reasoning, rule based reasoning, bayes, sistem pakar, demam berdarah},
  abstract  = {Penyakit demam berdarah merupakan salah satu penyakit menular yang sering menimbulkan wabah dan menyebabkan kematian. Pada penelitian ini dibangun sistem pakar menggunakan metode Case Based Reasoning (CBR) dan Rule Based Reasoning (RBR). Pencocokan kasus menggunakan konsep similarity dan solusi terbaik diambil berdasarkan perhitungan probabilitas bayes. Aplikasi sistem pakar untuk diagnosis demam berdarah ini mencapai tingkat akurasi sebesar 92\%.}
}
```

Angka akurasi 92% di atas berasal dari penelitian Jatmiko dkk. (2017),
bukan merupakan akurasi aplikasi ini.

## Catatan penting

- Cosine similarity tidak diganti dengan metode lain.
- Tidak memakai NumPy, Pandas, scikit-learn, atau API eksternal.
- Nilai tidak dibulatkan sebelum perankingan; pembulatan hanya saat tampil.
- Hasil kemiripan adalah rekomendasi awal, bukan peluang diagnosis pasti.

## Catatan redesign tampilan

Tampilan mengikuti aplikasi referensi (navbar pil, hero gradien, tile gejala, lembar
laporan). Perubahan hanya pada `app.py`, `components/` (termasuk `theme.py` dan
`layout.py`), dan `.streamlit/config.toml`. Folder `core/`, `data/`, `utils/` dan
`tests/` tidak diubah. Streamlit minimal 1.39 (memakai `st.container(key=...)`).
