"""Implementasi manual Cosine Similarity sesuai logika yang diberikan pengguna.

Rumus:

    Cosine(A, B) = (A . B) / (||A|| x ||B||)

Perhitungan sengaja dilakukan dengan perulangan Python bawaan, tanpa NumPy,
Pandas, atau library machine learning, agar prosesnya dapat diaudit secara manual.
"""


def cosine_similarity(kasusbaru, kasus):
    """Mengembalikan (dot product, cosine similarity) untuk dua vektor.

    Fungsi ini adalah bentuk langsung dari kode Python yang diberikan pengguna.
    Penanganan pembagian dengan nol dilakukan dengan mengembalikan cosine 0.0.
    """

    dot = 0
    kuadrat_kasusbaru = 0
    kuadrat_kasus = 0

    for j in range(len(kasusbaru)):
        dot += kasusbaru[j] * kasus[j]
        kuadrat_kasusbaru += kasusbaru[j] ** 2
        kuadrat_kasus += kasus[j] ** 2

    # Menghitung panjang vektor
    panjang_kasusbaru = kuadrat_kasusbaru ** 0.5
    panjang_kasus = kuadrat_kasus ** 0.5

    # Menghitung cosine similarity
    if panjang_kasusbaru * panjang_kasus == 0:
        cosine = 0.0
    else:
        cosine = dot / (panjang_kasusbaru * panjang_kasus)

    return dot, cosine


def hitung_detail(kasusbaru, kasus):
    """Mengembalikan seluruh komponen perhitungan untuk keperluan transparansi.

    Nilai ``dot`` dan ``cosine`` tetap diambil dari ``cosine_similarity`` agar
    tidak ada perbedaan antara angka yang ditampilkan dan hasil perankingan.
    """

    dot, cosine = cosine_similarity(kasusbaru, kasus)

    kuadrat_kasusbaru = 0
    kuadrat_kasus = 0

    for j in range(len(kasusbaru)):
        kuadrat_kasusbaru += kasusbaru[j] ** 2
        kuadrat_kasus += kasus[j] ** 2

    panjang_kasusbaru = kuadrat_kasusbaru ** 0.5
    panjang_kasus = kuadrat_kasus ** 0.5
    penyebut = panjang_kasusbaru * panjang_kasus

    return {
        "dot": dot,
        "kuadrat_kasusbaru": kuadrat_kasusbaru,
        "kuadrat_kasus": kuadrat_kasus,
        "panjang_kasusbaru": panjang_kasusbaru,
        "panjang_kasus": panjang_kasus,
        "penyebut": penyebut,
        "cosine": cosine,
    }
