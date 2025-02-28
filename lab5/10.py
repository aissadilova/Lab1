import re

def match_a_b_zero_or_more(text):
    """Matches 'a' followed by zero or more 'b's."""
    return bool(re.fullmatch(r'ab*', text))

def match_a_b_two_to_three(text):
    """Matches 'a' followed by two to three 'b's."""
    return bool(re.fullmatch(r'ab{2,3}', text))

def find_lowercase_underscore(text):
    """Finds sequences of lowercase letters joined with an underscore."""
    return re.findall(r'\b[a-z]+_[a-z]+\b', text)

def find_upper_followed_by_lower(text):
    """Finds sequences of an uppercase letter followed by lowercase letters."""
    return re.findall(r'[A-Z][a-z]+', text)

def match_a_anything_b(text):
    """Matches 'a' followed by anything, ending in 'b'."""
    return bool(re.fullmatch(r'a.*b', text))

def replace_with_colon(text):
    """Replaces spaces, commas, or dots with a colon."""
    return re.sub(r'[\s,\.]', ':', text)

def snake_to_camel(text):
    """Converts snake_case to camelCase."""
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text)

def split_at_uppercase(text):
    """Splits a string at uppercase letters."""
    return re.split(r'(?=[A-Z])', text)

def insert_spaces_capitals(text):
    """Inserts spaces between words starting with capital letters."""
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

def camel_to_snake(text):
    """Converts camelCase to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

if __name__ == "__main__":
    print("Example 1:", match_a_b_zero_or_more("abbbbb"))
    print("Example 2:", match_a_b_two_to_three("abb"))
    print("Example 3:", find_lowercase_underscore("hello_world"))
    print("Example 4:", find_upper_followed_by_lower("Hello"))
    print("Example 5:", match_a_anything_b("axxxb"))
    print("Example 6:", replace_with_colon("Hello, world. Test"))
    print("Example 7:", snake_to_camel("hello_world_example"))
    print("Example 8:", split_at_uppercase("SplitAtUppercase"))
    print("Example 9:", insert_spaces_capitals("InsertSpacesBetweenWords"))
    print("Example 10:", camel_to_snake("camelCaseExample"))
