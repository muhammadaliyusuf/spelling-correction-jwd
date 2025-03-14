from math import floor

# function untuk menghitung nilai Jaro Distance dari string1 dan string2

def jaroDistance(string1, string2):

    # cek jika string1 dan string2 sama
    if (string1 == string2):
        return 1.0

    # panjang dari string1 dan string2
    len_string1 = len(string1)
    len_string2 = len(string2)

    # maximum distance dari karakter yang sama dapat dibenarkan
    max_distance = floor(max(len_string1, len_string2) / 2) - 1

    # menghitung jumlah karakter yang sama
    match = 0

    # membuat variabel list dengan nilai nol yang panjang indeksnya sesuai panjang string1 dan string2
    match_string1 = [0] * len(string1)
    match_string2 = [0] * len(string2)

    # mencari karakter yang sama dari string1 dan string2
    for i in range(len_string1):
        # cek karakter yang sama dapat dibenarkan dengan maximum distance
        # yang tidak lebih dari nilai max distance dari karakter satu sama lain
        for j in range(max(0, i - max_distance), min(len_string2, i + max_distance + 1)):
            # cek jika ada karakter yang sama dari string1 dan string2
            if (string1[i] == string2[j] and match_string2[j] == 0):    
                match_string1[i] = 1
                match_string2[j] = 1
                match += 1
                break

    # cek jika tidak ada karakter yang sama dari string1 dan string2
    if (match == 0):
        return 0.0

    # mencari jumlah transposisi
    transposition = 0
    pointer = 0

    for i in range(len_string1):

        if (match_string1[i]):

            # melewati karakter yang tidak sama dari string2
            while (match_string2[pointer] == 0):
                pointer += 1

            # cek transposisi karakter
            if (string1[i] != string2[pointer]):
                transposition += 1

            pointer += 1

    transposition = transposition // 2

    # return rumus perhitungan jaro distance
    return (match / len_string1 + match / len_string2 +
            (match - transposition) / match) / 3.0


# function Jaro-Winkler Distance
def jaroWinklerDistance(string1, string2):

    jaro_distance = jaroDistance(string1, string2)

    # cek jika nilai jaro distance di atas threshold
    if (jaro_distance > 0.7):

        # menghitung panjang prefiks yang sama dari string1 dan string2
        prefiks = 0

        for i in range(min(len(string1), len(string2))):

            # jika karakter si & string2 sama
            if (string1[i] == string2[i]):
                prefiks += 1

            else:
                break

        # set panjang prefiks maksimal 4
        prefiks = min(4, prefiks)

        # menghitung nilai Jaro-Winkler Distance
        jaro_distance += 0.1 * prefiks * (1 - jaro_distance)

    return jaro_distance
