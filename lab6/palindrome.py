def is_palindrome(s):
    return s == s[::-1]

slovo = input("Enter: ")
print ("Palindrome: " , is_palindrome(slovo))