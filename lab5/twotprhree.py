def match_a_b_two_to_three(text):
    return bool(re.fullmatch(r'ab{2,3}', text))