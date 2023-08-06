from reg.numbers import re_num_list
from reg.numberscales import re_number_scale_list
from reg.date import re_date_list
from reg.id import re_id_list
from reg.oov import format_word, vi_dict
import re
from nltk import word_tokenize
import nltk

try:
    word_tokenize('test')
except:
    nltk.download('punkt')


def get_re_idx(re_str, src_txt):
    p_list = [
        (re.compile("^(" + re_str + ")\s"), 1),
        (re.compile("\s(" + re_str + ")$"), 1),
        (re.compile("(?=(\s(" + re_str + ")\s))"), 2),
        (re.compile("^(" + re_str + ")$"), 1),
    ]
    dict_result = dict({})
    for (p, idx) in p_list:
        # print(p, idx)
        # print(p, list(p.finditer(src_txt)))
        for m in p.finditer(src_txt):
            dict_result["{}-{}".format(m.start(idx), len(m.group(idx)))] = m.group(idx)
    return dict_result


def extract_word_tag(txt, txt_tag):
    phrases = []
    phrases_tags = []

    current_tag = 'O'
    phrase = []
    for char, char_tag in zip(list(txt), txt_tag):
        if char_tag.split('-')[-1] != current_tag:
            if len(phrase) > 0:
                phrases.append(''.join(phrase))
                phrases_tags.append(current_tag)
            phrase = [char]
            current_tag = char_tag.split('-')[-1]
        else:
            phrase.append(char)
    if len(phrase) > 0:
        phrases.append(''.join(phrase))
        phrases_tags.append(current_tag)

    words, word_tags = [], []
    for w, t in zip(phrases, phrases_tags):
        list_words = w.strip().split()
        words.extend(list_words)
        if t == 'O':
            word_tags.extend(['O'] * len(list_words))
        else:
            word_tags.append('B-{}'.format(t))
            word_tags.extend(['I-{}'.format(t)] * (len(list_words) - 1))

    return words, word_tags


def tagging(txt, debug=False):
    txt = ' '.join(word_tokenize(txt))
    txt_tag = ['O'] * len(txt)

    # number
    regex_numer = []
    for re_num in re_num_list:
        result = get_re_idx(re_num, txt)
        if len(result) > 0:
            regex_numer.append(result)
    for rel in regex_numer:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-number'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-number'
    if debug:
        print(regex_numer)
    # date
    regex_date = []
    for re_date in re_date_list:
        result = get_re_idx(re_date, txt)
        if len(result) > 0:
            regex_date.append(result)

    for rel in regex_date:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-date'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-date'
    if debug:
        print(regex_date)
    # number + scale
    regex_numscale = []
    for re_num_scale in re_number_scale_list:
        result = get_re_idx(re_num_scale, txt)
        if len(result) > 0:
            regex_numscale.append(result)
    for rel in regex_numscale:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-numscale'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-numscale'
    if debug:
        print(regex_numscale)
    # id
    regex_id = []
    for re_id in re_id_list:
        result = get_re_idx(re_id, txt)
        if len(result) > 0:
            regex_id.append(result)
    if debug:
        print(regex_id)
    for rel in regex_id:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            if list(set(txt_tag[idx:idx + len_item])) == ['O']:
                txt_tag[idx] = 'B-id'
                for i in range(idx + 1, idx + len_item):
                    txt_tag[i] = 'I-id'
    # OOV
    chars = []
    word_idx = 0
    oov_words = []
    for idx, char in enumerate(list(txt)):
        if char != ' ':
            chars.append(char)
        else:
            if len(chars) > 0:
                word = ''.join(chars)
                # check oov
                if format_word(word) not in vi_dict:
                    oov_words.append(word)
                    if list(set(txt_tag[word_idx:word_idx + len(chars)])) == ['O']:
                        txt_tag[word_idx] = 'B-oov'
                        for i in range(word_idx + 1, word_idx + len(chars)):
                            txt_tag[i] = 'I-oov'
            chars = []
            word_idx = idx + 1
    if debug:
        print(oov_words)
    return extract_word_tag(txt, txt_tag)


if __name__ == "__main__":
    input_text = 'Hiện nay 02/2020 cả nước có 1 208 trường hợp dương tính với virus cúm A/H1N1, trong đó miền Nam dẫn đầu với 182 trường hợp.'
    # input_text = ' '.join(word_tokenize(input_text))
    print(input_text)
    tags = tagging(input_text)
    for p_i in tags:
        print(p_i)
