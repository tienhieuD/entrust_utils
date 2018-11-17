# -*- coding: utf-8 -*-


def trim_recursion(string):
    string = string.replace(SPACE_CHAR * 2, SPACE_CHAR)
    return trim_recursion(string) if SPACE_CHAR * 2 in string else string


SPACE_CHAR, CURRENCY, HUNDRED_UNIT = ' ', 'đồng', ['', 'mươi', 'trăm']
UNIT_NAME = ['', 'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'triệu tỷ', 'tỷ tỷ']
NUMBER_TO_STRING = {'0': 'không', '1': 'một', '2': 'hai', '3': 'ba', '4': 'bốn', '5': 'năm', '6': 'sáu', '7': 'bảy', '8': 'tám', '9': 'chín'}
REPLACE_WORD = {'không mươi': 'linh', 'linh không': '', 'mươi không': 'mươi', 'một mươi': 'mười', 'mươi bốn': 'mươi tư', 'mười năm': 'mười lăm', 'mươi một': 'mươi mốt', 'mươi năm': 'mươi lăm', }
REPLACE_WORD_2 = dict([(trim_recursion(SPACE_CHAR.join((NUMBER_TO_STRING['0'], HUNDRED_UNIT[2], unit_name, CURRENCY))), CURRENCY) for unit_name in UNIT_NAME])
REPLACE_WORD_3 = {'không trăm linh đồng': 'đồng', 'không trăm linh không đồng': 'đồng'}

def number2text_vn(n):
    """ Convert number to Vietnam currency """
    float_number = float(n) if not isinstance(n, float) else n
    integer_part = int(float_number)
    decimal_part = str(float_number).split('.')[1] if '.' in str(float_number) else 0

    def read_hundred(hundred_number_s='025'):
        res, index = '', 0
        for char in reversed(hundred_number_s):
            res = SPACE_CHAR.join((NUMBER_TO_STRING[char], HUNDRED_UNIT[index], res))
            index += 1
        return res

    def read_number(number_s='1600300444'):
        groups = [number_s[::-1][i:i + 3][::-1] for i in range(0, len(number_s), 3)]
        res, index = '', 0
        for hundred in groups:
            res = SPACE_CHAR.join((read_hundred(hundred), UNIT_NAME[index], res))
            index += 1
        return res

    def to_string(money):
        string_money = str(money) if not isinstance(money, str) else money
        string_money = read_number(string_money)
        return string_money

    string_integer = to_string(integer_part)
    string_decimal = to_string(decimal_part) if int(decimal_part) else ''
    comma = 'phẩy' if string_decimal else ''
    result = trim_recursion(SPACE_CHAR.join((string_integer, comma, string_decimal, CURRENCY)))

    # Replace wrong words
    for wrong_word, right_word in REPLACE_WORD.items():
        result = trim_recursion(result.replace(wrong_word, right_word))
    for wrong_word, right_word in REPLACE_WORD_2.items():
        result = trim_recursion(result.replace(trim_recursion(wrong_word), right_word))
    for wrong_word, right_word in REPLACE_WORD_3.items():
        result = trim_recursion(result.replace(trim_recursion(wrong_word), right_word))

    return result.strip()


if __name__ == '__main__':
    assert number2text_vn(7000000) == 'bảy triệu đồng'
    assert number2text_vn(7000001) == 'bảy triệu không trăm nghìn không trăm linh một đồng'
    assert number2text_vn(7600000) == 'bảy triệu sáu trăm nghìn đồng'
    assert number2text_vn(7650000) == 'bảy triệu sáu trăm năm mươi nghìn đồng'
    assert number2text_vn(7650203) == 'bảy triệu sáu trăm năm mươi nghìn hai trăm linh ba đồng'
    pass
