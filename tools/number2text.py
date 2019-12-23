def remove_double_space(string):
    if SPACE * 2 in string:
        string = string.replace(SPACE * 2, SPACE)
        return remove_double_space(string)
    return string


SPACE = " "
EMPTY_CHAR = ""
COMMA = "phẩy"
CURRENCY = "đồng"
HUNDRED_UNIT = (EMPTY_CHAR, "mươi", "trăm")
UNIT_NAME = (EMPTY_CHAR, "nghìn", "triệu", "tỷ", "nghìn tỷ", "triệu tỷ", "tỷ tỷ")
NUMBER_TO_STRING = {"0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn", "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín"}
REPLACE_WORD = dict(
    **{"không mươi": "linh", "linh không": EMPTY_CHAR, "mươi không": "mươi", "một mươi": "mười", "mươi bốn": "mươi tư", "mười năm": "mười lăm", "mươi một": "mươi mốt", "mươi năm": "mươi lăm", },
    **{remove_double_space("không trăm {unit} {currency}").format(unit=unit_name, currency=CURRENCY): CURRENCY for unit_name in UNIT_NAME},
    **{"không trăm linh đồng": "đồng", "không trăm linh không đồng": "đồng", "trăm linh nghìn": "trăm nghìn"},
    **{remove_double_space("không trăm {unit} không trăm").format(unit=unit): "không trăm" for unit in UNIT_NAME[1:]},
    **{"không trăm {unit}".format(unit=unit): EMPTY_CHAR for unit in UNIT_NAME[1:]})


def replace_word(string):
    string = remove_double_space(string)
    if any(wrong_word in string for wrong_word in REPLACE_WORD.keys()):
        for wrong_word, right_word in REPLACE_WORD.items():
            if wrong_word in string:
                string = string.replace(wrong_word, right_word)
        return replace_word(string)
    return string


def number2text_vn(number, with_currency=True):
    """ Convert number to Vietnam currency """
    float_number = float(number) if not isinstance(number, float) else number
    integer_part = int(float_number)
    decimal_part = str(float_number).split(".")[1] if "." in str(float_number) else 0

    def read_hundred(n):
        hundred_number_s = str(n) if not isinstance(n, float) else n
        res, i = EMPTY_CHAR, 0
        for char in reversed(hundred_number_s):
            res = SPACE.join((NUMBER_TO_STRING[char], HUNDRED_UNIT[i], res))
            i += 1
        return res

    def read_number(n):
        number_s = str(n) if not isinstance(n, float) else n
        hundred_groups = [number_s[::-1][i:i+3][::-1] for i in range(0, len(number_s), 3)]
        res, index = EMPTY_CHAR, 0
        for hundred in hundred_groups:
            res = SPACE.join((read_hundred(hundred), UNIT_NAME[index], res))
            index += 1
        return res

    def to_string(n):
        string_number = str(n) if not isinstance(n, str) else n
        return read_number(string_number)

    string_integer = to_string(integer_part)
    string_decimal = to_string(decimal_part) if int(decimal_part) else EMPTY_CHAR
    comma = COMMA if string_decimal else EMPTY_CHAR
    result = remove_double_space(SPACE.join((string_integer, comma, string_decimal, CURRENCY)))
    result = replace_word(result)
    if not with_currency:
        return result.split(CURRENCY)[0]
    result = result.strip()
    return result


if __name__ == "__main__":
    assert number2text_vn(15) == "mười lăm đồng"
    assert number2text_vn(21) == "hai mươi mốt đồng"
    assert number2text_vn(1000) == "một nghìn đồng"
    assert number2text_vn(1001) == "một nghìn không trăm linh một đồng"

    assert number2text_vn(7000000) == "bảy triệu đồng"
    assert number2text_vn(7000002) == "bảy triệu không trăm linh hai đồng"
    assert number2text_vn(7000020) == "bảy triệu không trăm hai mươi đồng"
    assert number2text_vn(7000200) == "bảy triệu hai trăm đồng"
    assert number2text_vn(7002000) == "bảy triệu không trăm linh hai nghìn đồng"
    assert number2text_vn(7020000) == "bảy triệu không trăm hai mươi nghìn đồng"
    assert number2text_vn(7200000) == "bảy triệu hai trăm nghìn đồng"

    assert number2text_vn(7000022) == "bảy triệu không trăm hai mươi hai đồng"
    assert number2text_vn(7000220) == "bảy triệu hai trăm hai mươi đồng"
    assert number2text_vn(7002200) == "bảy triệu không trăm linh hai nghìn hai trăm đồng"
    assert number2text_vn(7022000) == "bảy triệu không trăm hai mươi hai nghìn đồng"
    assert number2text_vn(7220000) == "bảy triệu hai trăm hai mươi nghìn đồng"

    assert number2text_vn(7000202) == "bảy triệu hai trăm linh hai đồng"
    assert number2text_vn(7002020) == "bảy triệu không trăm linh hai nghìn không trăm hai mươi đồng"
    assert number2text_vn(7020200) == "bảy triệu không trăm hai mươi nghìn hai trăm đồng"
    assert number2text_vn(7202000) == "bảy triệu hai trăm linh hai nghìn đồng"

    assert number2text_vn(7000222) == "bảy triệu hai trăm hai mươi hai đồng"
    assert number2text_vn(7002220) == "bảy triệu không trăm linh hai nghìn hai trăm hai mươi đồng"
    assert number2text_vn(7022200) == "bảy triệu không trăm hai mươi hai nghìn hai trăm đồng"
    assert number2text_vn(7222000) == "bảy triệu hai trăm hai mươi hai nghìn đồng"
    assert number2text_vn(7002022) == "bảy triệu không trăm linh hai nghìn không trăm hai mươi hai đồng"
    assert number2text_vn(7020220) == "bảy triệu không trăm hai mươi nghìn hai trăm hai mươi đồng"
    assert number2text_vn(7202200) == "bảy triệu hai trăm linh hai nghìn hai trăm đồng"
    assert number2text_vn(7020022) == "bảy triệu không trăm hai mươi nghìn không trăm hai mươi hai đồng"
    assert number2text_vn(7200220) == "bảy triệu hai trăm nghìn hai trăm hai mươi đồng"
    assert number2text_vn(7200022) == "bảy triệu hai trăm nghìn không trăm hai mươi hai đồng"
