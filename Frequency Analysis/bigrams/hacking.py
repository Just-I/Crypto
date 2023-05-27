import sys
sys.path.append('../')

import localeChecking as lc
import random

def shuffle(len):
    used = [False for i in range(len)]
    shuffled = []
    for i in range(len):
        next_iter = random.randint(1, len - i)
        j = 0
        cnt = 0
        while cnt < next_iter:
            if not used[j]:
                cnt = cnt + 1
            j = j + 1
        j = j - 1
        used[j] = True
        shuffled.append(j)
    return shuffled

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

def hack_bigrams(frequency, encrypted):
    encrypted_frequency = {}
    amount = 0
    for i in range(len(encrypted)):
        char = encrypted[i]
        if lc.check(char) and i < len(encrypted) - 1 and lc.check(encrypted[i + 1]):
            next_char = encrypted[i + 1]
            char = char.lower()
            next_char = next_char.lower()
            bigramm = char + next_char
            count = encrypted_frequency.get(bigramm, 0)
            encrypted_frequency[bigramm] = count + 1
            amount = amount + 1
    for bigram in encrypted_frequency.keys():
        encrypted_frequency[bigram] = encrypted_frequency[bigram] / amount
    best_match = {}
    accuracy = 0
    length = 26
    if lc.isRus():
        length = 32
    for i in range(length):
        for j in range(length):
            if frequency.get(lc.ntl(i) + lc.ntl(j), 0) == 0:
                frequency[lc.ntl(i) + lc.ntl(j)] = 0
            if encrypted_frequency.get(lc.ntl(i) + lc.ntl(j), 0) == 0:
                encrypted_frequency[lc.ntl(i) + lc.ntl(j)] = 0
    shuffled = shuffle(length)
    for bigram in encrypted_frequency.keys():
        shuffled_bigram = lc.ntl(shuffled[lc.ltn(bigram[0])]) + lc.ntl(shuffled[lc.ltn(bigram[1])])
        if frequency.get(shuffled_bigram, 0) == 0:
            frequency[shuffled_bigram] = 0
        accuracy += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
    for j in range(length):
        best_match[lc.ntl(j)] = lc.ntl(shuffled[j])
    #за одну итерацию рандомно меняем две буквы и смотрим, стало ли правдопобнее или нет, если да то оставляем
    for i in range(10000):
        first = random.randrange(0, length)
        second = random.randrange(0, length)
        while second == first:
            second = random.randrange(0, length)
        current_acc = 0
        prev_acc = 0
        #страшные вычисления которые я не осознал как вынести в общий код
        for j in range(length):
            bigram = lc.ntl(j) + lc.ntl(first)
            shuffled_bigram = lc.ntl(shuffled[j]) + lc.ntl(shuffled[second])
            current_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(j) + lc.ntl(second)
            shuffled_bigram = lc.ntl(shuffled[j]) + lc.ntl(shuffled[first])
            current_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(first) + lc.ntl(j)
            shuffled_bigram = lc.ntl(shuffled[second]) + lc.ntl(shuffled[j])
            current_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(second) + lc.ntl(j)
            shuffled_bigram = lc.ntl(shuffled[first]) + lc.ntl(shuffled[j])
            current_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
        for j in range(length):
            bigram = lc.ntl(j) + lc.ntl(first)
            shuffled_bigram = lc.ntl(shuffled[j]) + lc.ntl(shuffled[first])
            prev_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(j) + lc.ntl(second)
            shuffled_bigram = lc.ntl(shuffled[j]) + lc.ntl(shuffled[second])
            prev_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(first) + lc.ntl(j)
            shuffled_bigram = lc.ntl(shuffled[first]) + lc.ntl(shuffled[j])
            prev_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2
            bigram = lc.ntl(second) + lc.ntl(j)
            shuffled_bigram = lc.ntl(shuffled[second]) + lc.ntl(shuffled[j])
            prev_acc += (encrypted_frequency[bigram] - frequency[shuffled_bigram]) ** 2

        if current_acc < prev_acc:
            x = shuffled[first]
            shuffled[first] = shuffled[second]
            shuffled[second] = x
            accuracy -= prev_acc - current_acc
            for j in range(length):
                best_match[lc.ntl(j)] = lc.ntl(shuffled[j])
    return decrypt(best_match, encrypted)
        

name = input("File to hack: ")
name_output = input("File to save result: ")
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
decrypted = hack_bigrams(frequency, encrypted)
file_write = open(name_output, 'w',  encoding="utf-8")
file_write.write(decrypted)
file_write.close()
file.close()
