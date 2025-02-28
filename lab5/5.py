def match_a_anything_b(text):
    return bool(re.fullmatch(r'a.*b', text))