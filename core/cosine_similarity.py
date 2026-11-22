def cosine_similarity(kasusbaru, kasus):
    dot = 0
    kuadrat_kasusbaru = 0
    kuadrat_kasus = 0

    for j in range(len(kasusbaru)):
        dot += kasusbaru[j] * kasus[j]
        kuadrat_kasusbaru += kasusbaru[j] ** 2
        kuadrat_kasus += kasus[j] ** 2

    panjang_kasusbaru = kuadrat_kasusbaru ** 0.5
    panjang_kasus = kuadrat_kasus ** 0.5

    if panjang_kasusbaru * panjang_kasus == 0:
        cosine = 0.0
    else:
        cosine = dot / (panjang_kasusbaru * panjang_kasus)

    return dot, cosine


def hitung_detail(kasusbaru, kasus):
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