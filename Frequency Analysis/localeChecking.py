import re

def check(ch):
    if str(ch).isalpha():
        locale = open('locale.txt', 'r', encoding='utf-8').read()
        if locale == "RUS":
            return bool(re.search('[а-яА-Я]', str(ch)))
        elif locale == "EN":
            return bool(re.search('[a-zA-Z]', str(ch)))
        else:
            raise LanguageError('Unsupported language, onlu russian (RUS) and english (EN) supported')
    else:
        return False

#letter to number
def ltn(ch):
    locale = open('locale.txt', 'r', encoding='utf-8').read()
    if locale == "RUS":
        if ch.isupper():
            return ord(ch) - ord('А')
        else:
            return ord(ch) - ord('а')
    else:
        if ch.isupper():
            return ord(ch) - ord('A')
        else:
            return ord(ch) - ord('a')

#only lower letters returned, number to letter
def ntl(number):
    locale = open('locale.txt', 'r', encoding='utf-8').read()
    if locale == "RUS":
        return chr(number + ord('а'))
    else:
        return chr(number + ord('a'))

def isRus():
    return open('locale.txt', 'r', encoding='utf-8').read() == "RUS"

def isEn():
    return open('locale.txt', 'r', encoding='utf-8').read() == "EN"
