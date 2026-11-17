"""Pengujian logika Cosine Similarity dan CBR.

Jalankan dari folder proyek Streamlit:

    python -m unittest discover -s tests -v
"""

import unittest

from core import cbr
from core.cosine_similarity import cosine_similarity, hitung_detail
from data.dataset import DHF, P006
from utils.validation import (
    validasi_pasien,
    validasi_pilihan_gejala,
    validasi_vektor,
)


class TestCosineSimilarity(unittest.TestCase):
    def test_hasil_dhf_sesuai_logika_asli(self):
        hasil = cbr.hitung_cbr(DHF.contoh_kasus_baru, DHF.kasus_lama)

        dot_expected = [5, 6, 6, 4]
        cosine_expected = [
            0.7905694150,
            0.8660254038,
            0.8017837257,
            0.5773502692,
        ]

        for index, item in enumerate(hasil):
            self.assertEqual(item["dot"], dot_expected[index])
            self.assertAlmostEqual(item["cosine"], cosine_expected[index], places=9)
            self.assertAlmostEqual(
                item["persentase"], cosine_expected[index] * 100, places=7
            )

        self.assertEqual(cbr.kasus_terbaik(hasil)["kode"], "DHF2")

    def test_hasil_p006_sesuai_logika_asli(self):
        hasil = cbr.hitung_cbr(P006.contoh_kasus_baru, P006.kasus_lama)

        dot_expected = [2, 0, 4, 16, 0]
        cosine_expected = [
            0.1145196669,
            0.0,
            0.2236067977,
            0.8207826817,
            0.0,
        ]

        for index, item in enumerate(hasil):
            self.assertEqual(item["dot"], dot_expected[index])
            self.assertAlmostEqual(item["cosine"], cosine_expected[index], places=9)

        self.assertEqual(cbr.kasus_terbaik(hasil)["kode"], "P004")
        self.assertEqual(cbr.urutkan_hasil(hasil)[0]["kode"], "P004")

    def test_pembagian_dengan_nol(self):
        dot, cosine = cosine_similarity([0, 0, 0], [1, 1, 1])
        self.assertEqual(dot, 0)
        self.assertEqual(cosine, 0.0)

        dot, cosine = cosine_similarity([0, 0], [0, 0])
        self.assertEqual(dot, 0)
        self.assertEqual(cosine, 0.0)

    def test_detail_konsisten_dengan_fungsi_utama(self):
        vektor_pertama = DHF.kasus_lama[0]["vektor"]
        dot, cosine = cosine_similarity(DHF.contoh_kasus_baru, vektor_pertama)
        detail = hitung_detail(DHF.contoh_kasus_baru, vektor_pertama)

        self.assertEqual(detail["dot"], dot)
        self.assertEqual(detail["cosine"], cosine)
        self.assertEqual(detail["kuadrat_kasusbaru"], 8)
        self.assertEqual(detail["kuadrat_kasus"], 5)

    def test_validasi_jumlah_atribut(self):
        with self.assertRaises(ValueError):
            validasi_vektor([1, 2], [{"vektor": [1, 2, 3]}], 3)

    def test_validasi_nilai_non_angka(self):
        with self.assertRaises(ValueError):
            validasi_vektor([1, "ya", 0], [{"vektor": [1, 0, 1]}], 3)

    def test_validasi_dataset_asli(self):
        for dataset in (DHF, P006):
            self.assertTrue(
                validasi_vektor(
                    dataset.contoh_kasus_baru,
                    dataset.kasus_lama,
                    dataset.jumlah_atribut,
                )
            )

    def test_buat_kasus_baru_dhf(self):
        terpilih = ["G1", "G2", "G5", "G8", "G9", "G12", "G13", "G14"]
        self.assertEqual(
            cbr.buat_kasus_baru(terpilih, DHF.atribut), DHF.contoh_kasus_baru
        )

    def test_validasi_pasien(self):
        self.assertEqual(
            validasi_pasien("  Azhar  ", "34", "Laki-laki"),
            {"nama": "Azhar", "usia": 34, "jk": "Laki-laki"},
        )
        with self.assertRaises(ValueError):
            validasi_pasien("", 20, "Laki-laki")
        with self.assertRaises(ValueError):
            validasi_pasien("Azhar", 150, "Laki-laki")
        with self.assertRaises(ValueError):
            validasi_pasien("Azhar", 20, None)

    def test_validasi_pilihan_gejala(self):
        self.assertTrue(validasi_pilihan_gejala(["G1", "G8"], DHF.atribut))
        with self.assertRaises(ValueError):
            validasi_pilihan_gejala([], DHF.atribut)
        with self.assertRaises(ValueError):
            validasi_pilihan_gejala(["G99"], DHF.atribut)


if __name__ == "__main__":
    unittest.main()
