import sys
sys.path.append('../')

import localeChecking as lc
import random

def decrypt(match, encrypted):
    decrypted = ''
    for char in encrypted:
        if lc.check(char):
            f = char.isupper()
            new_char = match[char.lower()]
            if f:
                decrypted += new_char.upper()
            else:
                decrypted += new_char
        else:
            decrypted += char
    return decrypted

def sortDict(dictionary):
    sorted_list = []
    for key in dictionary.keys():
        temp = []
        temp.append(dictionary[key])
        temp.append(key)
        sorted_list.append(temp)
    return sorted(sorted_list)

def hack(frequency, encrypted):
    encrypted_frequency = {}
    amount = 0
    for char in encrypted:
        if lc.check(char):
            char = char.lower()
            count = encrypted_frequency.get(char, 0)
            encrypted_frequency[char] = count + 1
            amount = amount + 1
    for symbol in encrypted_frequency.keys():
        if frequency.get(symbol, 0) == 0:
            raise UnknownLetter('Unknown letters: ' + symbol)
    for symbol in frequency.keys():
        if encrypted_frequency.get(symbol, 0) == 0:
            encrypted_frequency[symbol] = 0
        else:
            encrypted_frequency[symbol] = encrypted_frequency[symbol] / amount
    sorted_frequency = sortDict(frequency)
    sorted_encrypted = sortDict(encrypted_frequency)
    best_match = {}
    accuracy = 0
    length = 26
    if lc.isRus():
        length = 32
    shuffled = [0 for i in range(length)]
    for i in range(len(frequency.keys())):
        best_match[sorted_encrypted[i][1]] = sorted_frequency[i][1]
        shuffled[lc.ltn(sorted_encrypted[i][1])] = lc.ltn(sorted_frequency[i][1])
        accuracy += (frequency[sorted_encrypted[i][1]] - encrypted_frequency[sorted_frequency[i][1]]) ** 2
    for i in range(10000):
        first = random.randrange(0, length)
        second = random.randrange(0, length)
        while second == first:
            second = random.randrange(0, length)
        current_acc = (encrypted_frequency[lc.ntl(first)] - frequency[lc.ntl(shuffled[second])]) ** 2
        current_acc += (encrypted_frequency[lc.ntl(second)] - frequency[lc.ntl(shuffled[first])]) ** 2
        prev_acc = (encrypted_frequency[lc.ntl(first)] - frequency[lc.ntl(shuffled[first])]) ** 2
        prev_acc += (encrypted_frequency[lc.ntl(second)] - frequency[lc.ntl(shuffled[second])]) ** 2

        if current_acc < prev_acc:
            x = shuffled[first]
            shuffled[first] = shuffled[second]
            shuffled[second] = x
            accuracy -= prev_acc - current_acc
            for j in range(length):
                best_match[lc.ntl(j)] = lc.ntl(shuffled[j])
    return decrypt(best_match, encrypted)
        

name = input('File to hack: ')
output_name = input('File to save result: ')
name_frequency = input("File with dictionary of frequency: ")
file = open(name, 'r', encoding="utf-8")
encrypted = file.read()
frequency_file = open(name_frequency, 'r', encoding="utf-8")
frequency = {}
text = frequency_file.read().split()
i = 0
while i < len(text):
    frequency[text[i]] = float(text[i + 1])
    i = i + 2
decrypted = hack(frequency, encrypted)
file_write = open(output_name, 'w',  encoding="utf-8")
file_write.write(decrypted)
file_write.close()
file.close()
