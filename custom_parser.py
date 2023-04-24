from typing import Optional, Union
import lxml
import requests
from bs4 import BeautifulSoup
from word_dict import LETTER_DICT
import pandas as pd


def get_page_content1(s1: int) -> BeautifulSoup:
    DICT_URL = f"https://slovnyk.ua/index.php?s1={str(s1)}&s2=0"
    req = requests.get(DICT_URL)
    soup = BeautifulSoup(req.text, "lxml")
    return soup


def get_page_content2(s1: int, s2:int) -> BeautifulSoup:
    DICT_URL = f"https://slovnyk.ua/index.php?s1={str(s1)}&s2={str(s2)}"
    req = requests.get(DICT_URL)
    soup = BeautifulSoup(req.text, "lxml")
    return soup

def find_word_with_letters(letters: Union[list], words: Union[list]):
    res_words = []
    for word in words:
        counter = 0
        for letter in letters:
            if letter in word:
                counter += 1

        if counter == len(letters):
            res_words.append(word)
    return res_words

def find_all_words_from_web(letters: Union[str, list], numb_letters: Union[int, list], word_len: int):

    if isinstance(letters, str):
        letters = list(letters)

    if isinstance(numb_letters, int):
        numb_letters = list(numb_letters)
    res_words = []
    for letter in set(numb_letters):
        cont = get_page_content1(letter)
        cont = cont.find_all('a', {'class': 'cont_link'})
        print(len(cont))
        for i in range(1, len(cont)+1):
            cont2 = get_page_content2(letter, i)
            elems = cont2.find_all('p', {'class': 'cont_p'})
            for word in elems:
                if len(word.text) == word_len:
                    res_words.append(word.text)
    return res_words


def find_word_from_web(exactly_in_word: Union[str, list],
              exactly_not_in_word: Union[str, list],
              first_letter=None,
              word_len=5,
              is_all_letter_in_word=True):

    finish_words = []

    if isinstance(exactly_in_word, str):
        exactly_in_word = list(exactly_in_word)

    if isinstance(exactly_not_in_word, str):
        exactly_not_in_word = list(exactly_not_in_word)

    numb_exactly_in_word = []
    for l in exactly_in_word:
        numb_exactly_in_word.append(LETTER_DICT[l])

    numb_exactly_not_in_word = []
    for l in exactly_not_in_word:
        numb_exactly_not_in_word.append(LETTER_DICT[l])

    if first_letter:
        numb_first_letter = LETTER_DICT[first_letter]
    else:
        supposed_first_letters = []
        for l in LETTER_DICT.keys():
            if l not in exactly_not_in_word:
                supposed_first_letters.append(l)

        numb_supposed_first_letters = []
        for l in supposed_first_letters:
            numb_supposed_first_letters.append(LETTER_DICT[l])

    if first_letter:
        all_words = find_all_words_from_web(letters=first_letter,
                                   numb_letters=numb_first_letter,
                                   word_len=word_len)
    else:

        all_words = find_all_words_from_web(letters=supposed_first_letters,
                                   numb_letters=numb_supposed_first_letters,
                                   word_len=word_len)

    if is_all_letter_in_word:
        finish_words = find_word_with_letters(exactly_in_word, all_words)
        return finish_words

    return all_words


def find_words_with_options(df: pd.DataFrame,
                            exactly_in_word: Union[str, list, None] = None,
                            exactly_not_in_word: Union[str, list, None] = None,
                            letters_pos: Union[dict, None] = None,
                            letters_out_pos: Union[dict, None] = None,
                            word_len=5):

    if isinstance(exactly_in_word, str):
        exactly_in_word = list(exactly_in_word)

    if isinstance(exactly_not_in_word, str):
        exactly_not_in_word = list(exactly_not_in_word)

    if letters_pos:
        for k, v in letters_pos.items():
            df = df[df['word'].str[k] == v]
    # print(df)

    if exactly_in_word:
        regex_exactly_in_word = ''
        for l in exactly_in_word:
            regex_exactly_in_word = regex_exactly_in_word + f"(?=.*{l})"
        df = df[df['word'].str.contains(regex_exactly_in_word, regex=True)]
    # print(df)

    if exactly_not_in_word:
        q = ''.join(exactly_not_in_word)
        df = df[df['word'].str.contains(f'^(?!.*[{q}]).*$', regex=True)]

    if letters_out_pos:
        for k, v in letters_out_pos.items():
            df = df[df['word'].str[k] != v]

    return df['word'].values.tolist()



def write_all_words():
        letters = list(LETTER_DICT.keys())
        numb_letters = list(LETTER_DICT.values())
        print(letters, ":", numb_letters)
        all_words = find_all_words_from_web(letters, numb_letters, 5)
        df = pd.DataFrame(data={'word': all_words})
        df.to_csv("D:/python/dictionaryParser/words.csv", index=True)