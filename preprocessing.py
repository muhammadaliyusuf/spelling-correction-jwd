# function preprocessing text
def preprocessingtext(kalimat, daftar_kata_stopword):

    # Case Folding
    lower_case = kalimat.lower()

    # Cleaning (Menghapus Karakter whitespace)
    kalimat = lower_case.strip()

    # Cleaning (Menghapus Karakter simbol & tanda baca)
    punctuation = '''!()-[]}{;:'"\|,.<>/?@#$%^&*_`~'''

    cleaning_punctuation = ""
    for char in kalimat:
        if (char not in punctuation):
            cleaning_punctuation = cleaning_punctuation + char

    # Cleaning (Menghapus Karakter Angka)
    cleaning_number = ""
    for char in cleaning_punctuation:
        if not char.isdigit():
            cleaning_number = cleaning_number + char

    # Tokenizing
    tokens = cleaning_number.split()

    stp = []
    for i in tokens:
        if i not in daftar_kata_stopword:
            stp.append(i)

    return stp