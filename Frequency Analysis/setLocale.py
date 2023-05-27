language = input('Set language, EN for english and RUS for Russian: ')
f = open('locale.txt', 'w', encoding="utf-8")
f1 = open('./bigrams/locale.txt', 'w', encoding="utf-8")
f2 = open('./symbols/locale.txt', 'w', encoding="utf-8")
if language == 'EN' or language == 'RUS':
    f.write(language)
    f1.write(language)
    f2.write(language)
else:
    print('Unsupported language')
f.close()
f1.close()
f2.close()
