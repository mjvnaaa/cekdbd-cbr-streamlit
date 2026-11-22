# Manifest Paket Konteks AI

**Nama paket:** `Konteks-Proyek-SPK-CBR.zip`  
**Dibuat:** 21 November 2026  
**Tujuan:** Membantu AI memahami project SPK CBR/Cosine Similarity sebelum menyusun laporan proyek akhir.

---

## Cara pakai

1. Ekstrak ZIP ke folder kosong.
2. Berikan `PROMPT_LAPORAN_AKHIR.md` sebagai instruksi utama kepada AI.
3. Lampirkan seluruh file lain di dalam paket sebagai referensi pendukung.
4. Jika AI menanyakan data yang tidak ada di paket ini (misalnya nama dosen atau tanggal ujian), jawab langsung; jangan biarkan AI mengarang.

---

## Daftar file

| File | Alasan disertakan |
|---|---|
| `PROMPT_LAPORAN_AKHIR.md` | Prompt utama siap salin-tempel untuk generate laporan |
| `MANIFEST_KONTEKS.md` | File ini; menjelaskan isi paket |
| `README.md` | Identitas awal repository |
| `requirements.txt` | Bukti bahwa Streamlit adalah satu-satunya dependency eksternal |
| `app.py` | Entry point dan alur navigasi Streamlit |
| `core/__init__.py` | Penanda paket inti |
| `core/cosine_similarity.py` | Rumus manual dot product, kuadrat, akar, cosine |
| `core/cbr.py` | Pembentukan vektor, perbandingan kasus, ranking, kasus terbaik |
| `data/__init__.py` | Penanda paket data |
| `data/dataset.py` | Dataset DHF dan P006 beserta metadata |
| `utils/__init__.py` | Penanda paket utilitas |
| `utils/validation.py` | Validasi vektor, pasien, dan pilihan gejala |
| `components/__init__.py` | Penanda paket komponen UI |
| `components/dashboard.py` | Halaman awal dan penjelasan metode |
| `components/input_form.py` | Alur input dan pemanggilan fungsi CBR |
| `components/info_view.py` | Identitas akademik, referensi, tampilan dataset |
| `components/layout.py` | Navbar, stepper, footer, label grade |
| `components/result_view.py` | Tampilan hasil dan grafik perbandingan |
| `components/theme.py` | CSS, ikon, escaping HTML |
| `tests/test_cosine_similarity.py` | 10 unit test + nilai acuan perhitungan |
| `docs/README.md` | Panduan menjalankan, deploy, struktur, identitas |
| `docs/AUDIT_PROYEK_LAMA.md` | Hasil audit project HTML/JS sebelum migrasi |
| `docs/DOKUMENTASI_PERHITUNGAN.md` | Penelusuran angka perhitungan DHF dan P006 |
| `docs/PERBANDINGAN_JS_PYTHON.md` | Perbandingan implementasi lama dan Python |
| `docs/AUDIT_CBR_IMPLEMENTASI.md` | Audit 21 November 2026 (baru) |
| `docs/KODE_DASAR_CBR_PENGGUNA.md` | Kode acuan asli dari Penulis (baru) |

---

## File baru yang ditambahkan saat pembuatan paket

1. `PROMPT_LAPORAN_AKHIR.md`
2. `MANIFEST_KONTEKS.md`
3. `docs/AUDIT_CBR_IMPLEMENTASI.md`
4. `docs/KODE_DASAR_CBR_PENGGUNA.md`

Tidak ada baris kode pada `app.py`, `core/`, `data/`, `utils/`, `components/`, atau `tests/` yang diubah.

---

## Sengaja tidak disertakan

- `venv/` — ukuran besar, tidak relevan untuk pemahaman logika.
- `.git/` — metadata versi, bukan source code aplikasi.
- `.streamlit/config.toml` — hanya konfigurasi warna tema, tidak memengaruhi perhitungan.

---

## Ringkasan singkat untuk AI

Project ini adalah aplikasi Streamlit untuk mencocokkan gejala DHF pasien dengan 4 kasus rujukan gradeDHF memakai Cosine Similarity. Seluruh perhitungan ditulis manual di `core/cosine_similarity.py` dan `core/cbr.py`. Tidak ada NumPy/Pandas/scikit-learn. Dataset DHF ber-14 atribut biner; dataset P006 ber-19 atribut berbobot tersimpan sebagai contoh tambahan dan teruji, tetapi belum ditampilkan di UI. Database belum diintegrasikan dan harus disebut sebagai rencana, bukan fitur yang sudah ada.
