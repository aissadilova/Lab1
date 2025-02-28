def split_at_uppercase(text):
    return re.split(r'(?=[A-Z])', text)