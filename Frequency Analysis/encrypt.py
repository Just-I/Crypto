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

file = open(input('File to encrypt: '), 'r', encoding="utf-8")
name_output = input('File to save result: ')
text = file.read()
alphabet_length = 26
if lc.isRus():
    alphabet_length = 32
shuffled = shuffle(alphabet_length)
encrypted = ''
for char in text:
    if lc.check(char):
        f = char.isupper()
        new_char = lc.ntl(shuffled[lc.ltn(char)])
        if f:
            encrypted += new_char.upper()
        else:
            encrypted += new_char
    else:
        encrypted += char
file_write = open(name_output, 'w', encoding="utf-8")
file_write.write(encrypted)
file.close()
file_write.close()
