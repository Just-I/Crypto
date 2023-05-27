import sys
sys.path.append('../')

import localeChecking as lc

dictionary = {}
file_name = input('Example file to count letters frequency: ')
output_name = input('File to print results: ')
file = open(file_name, 'r', encoding="utf-8")
text = file.read()
amount = 0
for char in text:
    if str(char).isalpha() and lc.check(char):
        char = char.lower()
        count = dictionary.get(char, 0)
        dictionary[char] = count + 1
        amount = amount + 1
file_write = open(output_name, 'w', encoding="utf-8")
for key in dictionary.keys():
    file_write.write(key + ' ' + str(dictionary[key]/amount) + '\n')
file.close()
file_write.close()
