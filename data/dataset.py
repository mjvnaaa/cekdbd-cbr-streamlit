from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Dataset:
    key: str
    nama: str
    judul: str
    deskripsi: str
    kode_atribut: List[str]
    nama_atribut: List[str]
    kode_kasus: List[str]
    nama_kasus: List[str]
    vektor_kasus: List[List[int]]
    contoh_kasus_baru: List[int]
    tipe_input: str
    nilai_opsi: Tuple[int, ...]
    label_nilai: Dict[int, str]
    sumber: str

    @property
    def jumlah_atribut(self) -> int:
        return len(self.kode_atribut)

    @property
    def jumlah_kasus(self) -> int:
        return len(self.kode_kasus)

    @property
    def atribut(self) -> List[dict]:
        """Atribut sebagai daftar dict ``{"kode", "nama"}`` (dipakai komponen UI)."""
        return [
            {"kode": kode, "nama": nama}
            for kode, nama in zip(self.kode_atribut, self.nama_atribut)
        ]

    @property
    def kasus_lama(self) -> List[dict]:
        """Kasus rujukan awal sebagai daftar dict ``{"kode", "nama", "vektor"}``."""
        return [
            {"kode": kode, "nama": nama, "vektor": list(vektor)}
            for kode, nama, vektor in zip(
                self.kode_kasus, self.nama_kasus, self.vektor_kasus
            )
        ]


# ============================================================
# DATASET DHF
# ============================================================

KODE_GEJALA_DHF = [
    "G1", "G2", "G3", "G4", "G5", "G6", "G7",
    "G8", "G9", "G10", "G11", "G12", "G13", "G14",
]

NAMA_GEJALA_DHF = [
    "Demam", "Mual", "Muntah", "Lemas", "Mencret",
    "Kejang", "Tenggorokan Sakit", "Bintik Merah",
    "Mimisan", "Nyeri Sendi", "Pusing", "Leukosit",
    "Hematokrit", "Trombosit",
]

KODE_KASUS_DHF = ["DHF1", "DHF2", "DHF3", "DHF4"]

NAMA_KASUS_DHF = [
    "Demam Berdarah Grade I",
    "Demam Berdarah Grade II",
    "Demam Berdarah Grade III",
    "Demam Berdarah Grade IV",
]

VEKTOR_KASUS_DHF = [
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
]

KASUSBARU_DHF = [
    1, 1, 0, 0, 1, 0, 0,
    1, 1, 0, 0, 1, 1, 1,
]


# ============================================================
# DATASET P006
# ============================================================

KODE_ATRIBUT_P006 = [f"F{i}" for i in range(1, 20)]
NAMA_ATRIBUT_P006 = [f"Fitur {i}" for i in range(1, 20)]

KODE_KASUS_P006 = ["P001", "P002", "P003", "P004", "P005"]

NAMA_KASUS_P006 = [
    "Gastritis", "Maag", "Kanker Lambung",
    "Tumor Lambung", "GERD",
]

VEKTOR_KASUS_P006 = [
    [0, 0, 0, 0, 0, 0, 0, 3, 1, 5, 1, 0, 0, 0, 0, 5, 0, 0, 0],
    [1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 3, 5, 0, 0, 5, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
]

KASUSBARU_P006 = [
    0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
    1, 0, 0, 0, 0, 0, 0, 1, 0,
]


# ============================================================
# DATASET DEFINITIONS
# ============================================================

DHF = Dataset(
    key="dhf",
    nama="DHF (Demam Berdarah)",
    judul="Kemiripan Grade Demam Berdarah",
    deskripsi=(
        "Empat kasus rujukan grade DHF dengan 14 gejala biner. "
        "Nilai 1 berarti gejala ada, 0 berarti tidak ada."
    ),
    kode_atribut=KODE_GEJALA_DHF,
    nama_atribut=NAMA_GEJALA_DHF,
    kode_kasus=KODE_KASUS_DHF,
    nama_kasus=NAMA_KASUS_DHF,
    vektor_kasus=VEKTOR_KASUS_DHF,
    contoh_kasus_baru=KASUSBARU_DHF,
    tipe_input="binary",
    nilai_opsi=(0, 1),
    label_nilai={0: "Tidak ada", 1: "Ada"},
    sumber="js/data.js; Jatmiko, Junaedi, dan Imrona (2017), Tabel 2-1 sampai 2-3.",
)

P006 = Dataset(
    key="p006",
    nama="P006 (Penyakit Lambung)",
    judul="Kemiripan Kasus P006",
    deskripsi=(
        "Lima kasus lama penyakit lambung dengan 19 atribut berbobot. "
        "Kasus baru contoh memakai nilai 0/1, sedangkan kasus lama "
        "memakai 0/1/3/5. Nama atribut tidak tersedia di kode sumber, "
        "sehingga ditampilkan sebagai F1-F19."
    ),
    kode_atribut=KODE_ATRIBUT_P006,
    nama_atribut=NAMA_ATRIBUT_P006,
    kode_kasus=KODE_KASUS_P006,
    nama_kasus=NAMA_KASUS_P006,
    vektor_kasus=VEKTOR_KASUS_P006,
    contoh_kasus_baru=KASUSBARU_P006,
    tipe_input="bobot",
    nilai_opsi=(0, 1, 3, 5),
    label_nilai={0: "0", 1: "1", 3: "3", 5: "5"},
    sumber="Kode Python P006 yang diberikan pengguna (tanpa daftar nama atribut).",
)


# ============================================================
# DATASET REGISTRY
# ============================================================

DAFTAR_DATASET = [DHF, P006]


def get_dataset(key):
    for dataset in DAFTAR_DATASET:
        if dataset.key == key:
            return dataset

    raise KeyError(f"Dataset '{key}' tidak ditemukan.")