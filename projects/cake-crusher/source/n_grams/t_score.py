from math import pow


def t_score(threegram, freqs_dict, dictionary):
    n = 3
    count = freqs_dict[threegram]
    multiplication = 1
    for lemma in threegram:
        lemma_id = dictionary.token2id[lemma]
        multiplication *= dictionary.cfs[lemma_id]
    part = multiplication / pow(dictionary.num_pos, n - 1)
    return (count - part) / pow(count, 1 / n)
