def find_lowercase_underscore(text):
    return re.findall(r'\b[a-z]+_[a-z]+\b', text)
