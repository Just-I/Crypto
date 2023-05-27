import sys
sys.path.append('../')

import localeChecking as lc

dictionary = {}
file_name = input('Example file for counting bigrams: ')
output_name = input('File to print results: ')
file = open(file_name, 'r', encoding="utf-8")
text = file.read()
amount = 0
for i in range(len(text)):
    char = text[i]
    if lc.check(char) and i < len(text) - 1 and lc.check(text[i + 1]):
        next_char = text[i + 1]
        char = char.lower()
        next_char = next_char.lower()
        bigramm = char + next_char
        count = dictionary.get(bigramm, 0)
        dictionary[bigramm] = count + 1
        amount = amount + 1
file_write = open(output_name, 'w', encoding="utf-8")
for key in dictionary.keys():
    file_write.write(key + ' ' + str(dictionary[key]/amount) + '\n')
file.close()
file_write.close()
