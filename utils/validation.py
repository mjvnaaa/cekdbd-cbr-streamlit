"""Validasi input sebelum perhitungan dijalankan."""

from numbers import Number


def _vektor_dari(kasus):
    return kasus["vektor"] if isinstance(kasus, dict) else kasus


def validasi_vektor(kasusbaru, kasus_lama, jumlah_atribut=None):
    """Memastikan jumlah atribut dan tipe nilai valid.

    Melempar ``ValueError`` ketika:
    - jumlah atribut kasus baru tidak sesuai;
    - salah satu kasus lama memiliki panjang vektor berbeda;
    - terdapat nilai yang bukan angka.
    """

    if jumlah_atribut is None:
        jumlah_atribut = len(kasusbaru)

    if len(kasusbaru) != jumlah_atribut:
        raise ValueError(
            f"Kasus baru memiliki {len(kasusbaru)} atribut, "
            f"seharusnya {jumlah_atribut}."
        )

    for i, nilai in enumerate(kasusbaru):
        if isinstance(nilai, bool) or not isinstance(nilai, Number):
            raise ValueError(f"Nilai kasus baru ke-{i + 1} bukan angka: {nilai!r}")

    for index, kasus in enumerate(kasus_lama):
        vektor = _vektor_dari(kasus)
        if len(vektor) != jumlah_atribut:
            raise ValueError(
                f"Kasus lama ke-{index + 1} memiliki {len(vektor)} atribut, "
                f"seharusnya {jumlah_atribut}."
            )
        for i, nilai in enumerate(vektor):
            if isinstance(nilai, bool) or not isinstance(nilai, Number):
                raise ValueError(
                    f"Nilai kasus lama ke-{index + 1}, atribut ke-{i + 1} "
                    f"bukan angka: {nilai!r}"
                )

    return True


def validasi_pasien(nama, usia, jenis_kelamin):
    """Memeriksa data diri yang diisi pengguna awam.

    Mengembalikan dict pasien yang sudah rapi, atau melempar ``ValueError``
    dengan pesan yang mudah dipahami pengguna.
    """

    nama = str(nama or "").strip()
    if not nama:
        raise ValueError("Nama lengkap wajib diisi.")

    try:
        usia = int(usia)
    except (TypeError, ValueError):
        raise ValueError("Usia harus berupa angka.")

    if usia < 0 or usia > 120:
        raise ValueError("Usia harus antara 0 sampai 120 tahun.")

    if jenis_kelamin not in ("Laki-laki", "Perempuan"):
        raise ValueError("Pilih jenis kelamin terlebih dahulu.")

    return {"nama": nama, "usia": usia, "jk": jenis_kelamin}


def validasi_pilihan_gejala(terpilih, atribut):
    """Memastikan sedikitnya satu gejala dipilih dan kodenya dikenal."""

    if not terpilih:
        raise ValueError("Pilih sedikitnya satu gejala yang dialami.")

    kode_valid = {item["kode"] for item in atribut}
    for kode in terpilih:
        if kode not in kode_valid:
            raise ValueError(f"Kode gejala '{kode}' tidak dikenal.")

    return True
