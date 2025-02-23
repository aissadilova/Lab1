def match_a_b_zero_or_more(text):
    return bool(re.fullmatch(r'ab*', text))