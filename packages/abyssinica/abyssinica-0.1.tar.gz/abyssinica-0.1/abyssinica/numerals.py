_digit_map = {
    0: '',
    1: '፩',
    2: '፪',
    3: '፫',
    4: '፬',
    5: '፭',
    6: '፮',
    7: '፯',
    8: '፰',
    9: '፱',
    10: '፲',
    20: '፳',
    30: '፴',
    40: '፵',
    50: '፶',
    60: '፷',
    70: '፸',
    80: '፹',
    90: '፺',
    100: '፻',
    10000: '፼'
}

_reverse_digit_map = {
    '፩': 1,
    '፪': 2,
    '፫': 3,
    '፬': 4,
    '፭': 5,
    '፮': 6,
    '፯': 7,
    '፰': 8,
    '፱': 9,
    '፲': 10,
    '፳': 20,
    '፴': 30,
    '፵': 40,
    '፶': 50,
    '፷': 60,
    '፸': 70,
    '፹': 80,
    '፺': 90,
    '፻': 100,
    '፼': 10000
}

_digit_map_ascii = {
    0: '',
    1: '{1}',
    2: '{2}',
    3: '{3}',
    4: '{4}',
    5: '{5}',
    6: '{6}',
    7: '{7}',
    8: '{8}',
    9: '{9}',
    10: '{10}',
    20: '{20}',
    30: '{30}',
    40: '{40}',
    50: '{50}',
    60: '{60}',
    70: '{70}',
    80: '{80}',
    90: '{90}',
    100: '{100}',
    10000: '{10,000}'
}


def arabic_to_geez(num):
    assert (isinstance(num, int))
    assert (num > 0)

    return _arabic_to_geez(num, _digit_map)


def arabic_to_geez_ascii(num):
    assert (isinstance(num, int))
    assert (num > 0)

    return _arabic_to_geez(num, _digit_map_ascii)


def _arabic_to_geez(num, digit_map):
    if num >= 20000:
        # num is in the range [20,000, infinity]
        quotient = num // 10000
        remainder = num % 10000
        return _arabic_to_geez(quotient, digit_map) + digit_map[10000] + _arabic_to_geez(remainder, digit_map)

    elif num >= 10000:
        # num is in the range [10,000, 19,999]
        remainder = num % 10000
        return digit_map[10000] + _arabic_to_geez(remainder, digit_map)

    elif num >= 200:
        # num is in the range [200, 9,999]
        quotient = num // 100
        remainder = num % 100
        return _arabic_to_geez(quotient, digit_map) + digit_map[100] + _arabic_to_geez(remainder, digit_map)

    elif num >= 100:
        # num is in the range [100, 199]
        remainder = num % 100
        return digit_map[100] + _arabic_to_geez(remainder, digit_map)

    else:
        # num is in the range [1, 99]
        tens = num // 10 * 10
        ones = num % 10
        return digit_map[tens] + digit_map[ones]


def geez_to_arabic(num):
    assert (isinstance(num, str))

    return _geez_to_arabic_ten_thousands(num)


def _geez_to_arabic_ten_thousands(num):
    try:
        idx = num.rindex(_digit_map[10000])
        return (_geez_to_arabic_ten_thousands(num[:idx]) or 1) * 10000 + _geez_to_arabic_ten_thousands(num[idx + 1:])
    except ValueError:
        return _geez_to_arabic_one_hundreds(num)


def _geez_to_arabic_one_hundreds(num):
    try:
        idx = num.rindex(_digit_map[100])
        return (_geez_to_arabic_one_hundreds(num[:idx]) or 1) * 100 + _geez_to_arabic_one_hundreds(num[idx + 1:])
    except ValueError:
        return _geez_to_arabic_tens_and_ones(num)


def _geez_to_arabic_tens_and_ones(num):
    return sum([_reverse_digit_map[digit] for digit in num])

