def find_upper_followed_by_lower(text):
    return re.findall(r'[A-Z][a-z]+', text)