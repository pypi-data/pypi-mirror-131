

def whiteRm(st):
    return st.strip()


def cap_each(string):
    list_of_words = string.split(" ")

    for word in list_of_words:
        list_of_words[list_of_words.index(word)] = word.capitalize()

    return " ".join(list_of_words)
