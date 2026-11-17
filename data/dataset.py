"""Dataset resmi proyek.

Dataset DHF disalin dari ``js/data.js`` (nama gejala asli dari Jatmiko dkk., 2017).
Dataset P006 disalin dari kode Python yang diberikan pengguna. Karena kode sumber
tidak menyediakan nama atribut untuk P006, atributnya diberi kode F1 sampai F19.
Tidak ada nama gejala P006 yang dikarang di sini.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class Dataset:
    key: str
    nama: str
    judul: str
    deskripsi: str
    atribut: List[Dict[str, Any]]
    kasus_lama: List[Dict[str, Any]]
    contoh_kasus_baru: List[int]
    tipe_input: str = "binary"
    nilai_opsi: Tuple[int, ...] = (0, 1)
    label_nilai: Dict[int, str] = field(default_factory=dict)
    sumber: str = ""

    @property
    def jumlah_atribut(self) -> int:
        return len(self.atribut)

    @property
    def jumlah_kasus(self) -> int:
        return len(self.kasus_lama)


# ===== DATASET DHF (14 atribut, nilai 0/1) =====
# Sumber: js/data.js -> GEJALA dan KASUS_LAMA
GEJALA = [
    {"kode": "G1", "nama": "Demam"},
    {"kode": "G2", "nama": "Mual"},
    {"kode": "G3", "nama": "Muntah"},
    {"kode": "G4", "nama": "Lemas"},
    {"kode": "G5", "nama": "Mencret"},
    {"kode": "G6", "nama": "Kejang"},
    {"kode": "G7", "nama": "Tenggorokan Sakit"},
    {"kode": "G8", "nama": "Bintik Merah"},
    {"kode": "G9", "nama": "Mimisan"},
    {"kode": "G10", "nama": "Nyeri Sendi"},
    {"kode": "G11", "nama": "Pusing"},
    {"kode": "G12", "nama": "Leukosit"},
    {"kode": "G13", "nama": "Hematokrit"},
    {"kode": "G14", "nama": "Trombosit"},
]

KASUS_LAMA_DHF = [
    {
        "kode": "DHF1",
        "nama": "Demam Berdarah Grade I",
        "vektor": [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    },
    {
        "kode": "DHF2",
        "nama": "Demam Berdarah Grade II",
        "vektor": [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    },
    {
        "kode": "DHF3",
        "nama": "Demam Berdarah Grade III",
        "vektor": [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    },
    {
        "kode": "DHF4",
        "nama": "Demam Berdarah Grade IV",
        "vektor": [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    },
]

KASUSBARU_DHF_CONTOH = [1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]

DHF = Dataset(
    key="dhf",
    nama="DHF (Demam Berdarah)",
    judul="Kemiripan Grade Demam Berdarah",
    deskripsi=(
        "Empat kasus rujukan grade DHF dengan 14 gejala biner. "
        "Nilai 1 berarti gejala ada, 0 berarti tidak ada."
    ),
    atribut=GEJALA,
    kasus_lama=KASUS_LAMA_DHF,
    contoh_kasus_baru=KASUSBARU_DHF_CONTOH,
    tipe_input="binary",
    nilai_opsi=(0, 1),
    label_nilai={0: "Tidak ada", 1: "Ada"},
    sumber="js/data.js; Jatmiko, Junaedi, dan Imrona (2017), Tabel 2-1 sampai 2-3.",
)


# ===== DATASET P006 (19 atribut, bobot 0/1/3/5) =====
# Sumber: kode Python "kasus baru P006" yang diberikan pengguna.
P006_ATRIBUT = [
    {"kode": f"F{i}", "nama": f"Fitur {i}"} for i in range(1, 20)
]

KASUS_LAMA_P006 = [
    {
        "kode": "P001",
        "nama": "Gastritis",
        "vektor": [0, 0, 0, 0, 0, 0, 0, 3, 1, 5, 1, 0, 0, 0, 0, 5, 0, 0, 0],
    },
    {
        "kode": "P002",
        "nama": "Maag",
        "vektor": [1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
    },
    {
        "kode": "P003",
        "nama": "Kanker Lambung",
        "vektor": [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 3, 5, 0, 0, 5, 0, 1, 0, 0],
    },
    {
        "kode": "P004",
        "nama": "Tumor Lambung",
        "vektor": [0, 0, 0, 0, 0, 5, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    },
    {
        "kode": "P005",
        "nama": "GERD",
        "vektor": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    },
]

KASUSBARU_P006_CONTOH = [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]

P006 = Dataset(
    key="p006",
    nama="P006 (Penyakit Lambung)",
    judul="Kemiripan Kasus P006",
    deskripsi=(
        "Lima kasus lama penyakit lambung dengan 19 atribut berbobot. "
        "Kasus baru contoh memakai nilai 0/1, sedangkan kasus lama memakai 0/1/3/5. "
        "Nama atribut tidak tersedia di kode sumber, sehingga ditampilkan sebagai F1-F19."
    ),
    atribut=P006_ATRIBUT,
    kasus_lama=KASUS_LAMA_P006,
    contoh_kasus_baru=KASUSBARU_P006_CONTOH,
    tipe_input="bobot",
    nilai_opsi=(0, 1, 3, 5),
    label_nilai={0: "0", 1: "1", 3: "3", 5: "5"},
    sumber="Kode Python P006 yang diberikan pengguna (tanpa daftar nama atribut).",
)

DAFTAR_DATASET = [DHF, P006]


def get_dataset(key):
    """Mengambil dataset berdasarkan kunci."""

    for dataset in DAFTAR_DATASET:
        if dataset.key == key:
            return dataset
    raise KeyError(f"Dataset '{key}' tidak ditemukan.")
