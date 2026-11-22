"""Pengujian empat tahap siklus CBR: Retrieve, Reuse, Revise, Retain.

Jalankan dari folder proyek:

    python -m unittest discover -s tests -v
"""

import datetime
import os
import tempfile
import unittest

from core import basis_kasus, cbr
from data.dataset import DHF, P006


class TestSiklusCBR(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "basis.json")

    def tearDown(self):
        self.folder.cleanup()

    # ---------- Reuse ----------
    def test_reuse_mengusulkan_grade_kasus_terbaik(self):
        hasil = cbr.hitung_cbr(DHF.contoh_kasus_baru, DHF.kasus_lama)
        usulan = cbr.reuse(hasil)

        self.assertEqual(usulan["kode_kasus"], "DHF2")
        self.assertEqual(usulan["grade"], "Demam Berdarah Grade II")
        self.assertAlmostEqual(usulan["persentase"], 86.6025403784, places=7)
        self.assertFalse(usulan["perlu_ditinjau"])

    def test_reuse_tanpa_kemiripan_tidak_mengusulkan_grade(self):
        hasil = cbr.hitung_cbr([0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], DHF.kasus_lama)
        usulan = cbr.reuse(hasil)

        self.assertIsNone(usulan["grade"])
        self.assertTrue(usulan["perlu_ditinjau"])

    def test_reuse_kemiripan_rendah_perlu_ditinjau(self):
        kasusbaru = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        usulan = cbr.reuse(cbr.hitung_cbr(kasusbaru, DHF.kasus_lama))
        self.assertTrue(usulan["perlu_ditinjau"])

    def test_reuse_daftar_kosong(self):
        self.assertIsNone(cbr.reuse([]))

    # ---------- Revise ----------
    def _usulan_dhf(self):
        return cbr.reuse(cbr.hitung_cbr(DHF.contoh_kasus_baru, DHF.kasus_lama))

    def test_revise_menerima_usulan(self):
        revisi = cbr.revise(self._usulan_dhf(), "Demam Berdarah Grade II", DHF.nama_kasus)
        self.assertFalse(revisi["direvisi"])
        self.assertEqual(revisi["grade_final"], "Demam Berdarah Grade II")

    def test_revise_mengubah_grade(self):
        revisi = cbr.revise(
            self._usulan_dhf(), "Demam Berdarah Grade III", DHF.nama_kasus, "  dokter  "
        )
        self.assertTrue(revisi["direvisi"])
        self.assertEqual(revisi["grade_usulan"], "Demam Berdarah Grade II")
        self.assertEqual(revisi["catatan"], "dokter")

    def test_revise_menolak_grade_tidak_valid(self):
        with self.assertRaises(ValueError):
            cbr.revise(self._usulan_dhf(), "Grade Fiktif", DHF.nama_kasus)
        with self.assertRaises(ValueError):
            cbr.revise(self._usulan_dhf(), None, DHF.nama_kasus)
        with self.assertRaises(ValueError):
            cbr.revise(None, "Demam Berdarah Grade II", DHF.nama_kasus)

    # ---------- Retain ----------
    def _revisi(self, grade="Demam Berdarah Grade II"):
        return cbr.revise(self._usulan_dhf(), grade, DHF.nama_kasus)

    def test_basis_awal_hanya_kasus_rujukan(self):
        basis = basis_kasus.muat_basis(DHF, self.path)
        self.assertEqual([k["kode"] for k in basis], DHF.kode_kasus)

    def test_retain_menyimpan_dan_bertahan_di_berkas(self):
        baru = [1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        waktu = datetime.datetime(2026, 11, 22, 10, 0, 0)
        hasil = basis_kasus.retain(DHF, baru, self._revisi(), self.path, waktu)

        self.assertEqual(hasil["status"], "disimpan")
        self.assertEqual(hasil["kasus"]["kode"], "DHF2-K1")
        self.assertEqual(hasil["kasus"]["nama"], "Demam Berdarah Grade II")
        self.assertEqual(hasil["kasus"]["dibuat"], "2026-11-22T10:00:00")

        # dibaca ulang dari berkas (simulasi aplikasi dimuat ulang)
        basis = basis_kasus.muat_basis(DHF, self.path)
        self.assertEqual(len(basis), 5)
        self.assertEqual(basis[-1]["vektor"], baru)

    def test_retain_tidak_menyimpan_identitas_pasien(self):
        baru = [1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        hasil = basis_kasus.retain(DHF, baru, self._revisi(), self.path)
        self.assertEqual(
            set(hasil["kasus"]),
            {"kode", "nama", "vektor", "sumber", "direvisi", "catatan", "dibuat"},
        )

    def test_retain_menolak_duplikat(self):
        self.assertEqual(
            basis_kasus.retain(DHF, DHF.contoh_kasus_baru, self._revisi(), self.path)["status"],
            "disimpan",
        )
        ulang = basis_kasus.retain(DHF, DHF.contoh_kasus_baru, self._revisi(), self.path)
        self.assertEqual(ulang["status"], "duplikat")
        self.assertEqual(basis_kasus.jumlah_tersimpan(DHF, self.path), 1)

        # pola identik dengan kasus rujukan awal juga tidak disimpan
        rujukan = DHF.kasus_lama[1]
        hasil = basis_kasus.retain(
            DHF, rujukan["vektor"], self._revisi(rujukan["nama"]), self.path
        )
        self.assertEqual(hasil["status"], "duplikat")

    def test_retain_nomor_kode_bertambah(self):
        a = [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]
        b = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        kode_a = basis_kasus.retain(DHF, a, self._revisi(), self.path)["kasus"]["kode"]
        kode_b = basis_kasus.retain(DHF, b, self._revisi(), self.path)["kasus"]["kode"]
        self.assertEqual((kode_a, kode_b), ("DHF2-K1", "DHF2-K2"))

    def test_retain_validasi_input(self):
        with self.assertRaises(ValueError):
            basis_kasus.retain(DHF, [1, 0], self._revisi(), self.path)
        with self.assertRaises(ValueError):
            basis_kasus.retain(DHF, [0] * 14, self._revisi(), self.path)

    def test_retain_terpisah_per_dataset(self):
        basis_kasus.retain(DHF, DHF.contoh_kasus_baru, self._revisi(), self.path)
        self.assertEqual(basis_kasus.jumlah_tersimpan(P006, self.path), 0)
        self.assertEqual(len(basis_kasus.muat_basis(P006, self.path)), 5)

    def test_berkas_rusak_dianggap_kosong(self):
        with open(self.path, "w", encoding="utf-8") as berkas:
            berkas.write("{bukan json")
        self.assertEqual(len(basis_kasus.muat_basis(DHF, self.path)), 4)

    # ---------- siklus penuh ----------
    def test_kasus_tersimpan_dipakai_pada_retrieve_berikutnya(self):
        """Retain benar-benar mengubah hasil Retrieve (inti siklus CBR)."""
        # Kasus: gejala DHF2 ditambah G2 (Mual). Pakar menetapkan Grade III.
        baru = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1]

        sebelum = cbr.reuse(
            cbr.hitung_cbr(baru, basis_kasus.muat_basis(DHF, self.path))
        )
        self.assertEqual(sebelum["kode_kasus"], "DHF2")

        revisi = cbr.revise(sebelum, "Demam Berdarah Grade III", DHF.nama_kasus)
        self.assertTrue(revisi["direvisi"])
        basis_kasus.retain(DHF, baru, revisi, self.path)

        # Pasien berikutnya dengan pola yang sama kini cocok 100% ke kasus tersimpan.
        sesudah = cbr.reuse(
            cbr.hitung_cbr(baru, basis_kasus.muat_basis(DHF, self.path))
        )
        self.assertEqual(sesudah["kode_kasus"], "DHF3-K1")
        self.assertEqual(sesudah["grade"], "Demam Berdarah Grade III")
        self.assertAlmostEqual(sesudah["cosine"], 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
