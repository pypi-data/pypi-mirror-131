import os


def format_word(text):
    text = text.lower()
    text = text.replace('-', ' ')
    return text


def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().strip().split('\n')
    word_dict = []
    for word in words:
        word_formated = format_word(word)
        # word_dict.append(word_formated)
        word_dict.extend(word_formated.split())
    word_dict.extend(list('".,?!@#$%^&*()_-+=\';:<>/'))
    return set(word_dict)


vi_dict = load_dictionary(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vidict.txt'))
