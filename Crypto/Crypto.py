import argparse
import sys


class Text:
    def __init__(self, f = []):
        self.text = []
        for line in f:
            self.text.append(line)

class Crypto:
    def __init__(self):
        pass
    
    def IsBigLetter(self, symbol):
        if (ord(symbol) >= ord('A')) and (ord(symbol) <= ord('Z')):
            return True
        return False
    
    def IsSmallLetter(self, symbol):
        if (ord(symbol) >= ord('a')) and (ord(symbol) <= ord('z')):
            return True
        return False

    def IsLetter(self, symbol):
        if self.IsBigLetter(symbol) or self.IsSmallLetter(symbol):
            return True
        return False
        
    def CryptoLetter(self, letter, key):
        number = ord(letter)
        is_big = True
        if self.IsBigLetter(letter):
            number -= ord('A')
        else:
            is_big = False
            number -= ord('a')
        number += key
        number = number % 26
        if is_big:
            number += ord('A')
        else:
            number += ord('a')
        return chr(number)
            
    def CryptoLine(self, line, key):
        encrypted_line = ""
        j = 0
        for letter in line:
            if self.IsLetter(letter):
                encrypted_line += self.CryptoLetter(letter, key[j % len(key)])
                j += 1
                j = j % len(key)
            else:
                encrypted_line += letter
        return encrypted_line

    def NumberOfLetters(self, line):
        count = 0
        for letter in line:
            if self.IsBigLetter(letter) or self.IsSmallLetter(letter):
                count += 1
        return count
    
class Encryptor(Crypto):
    def EncryptCaesar(self, text, key):
        encrypted_text = Text()
        for line in text.text:
            encrypted_text.text.append(self.CryptoLine(line, [key]))
        return encrypted_text

    def EncryptVigenere(self, text, key):
        encrypted_text = Text()
        keys = []
        key = key.lower()
        for letter in key:
            keys.append(ord(letter) - ord('a'))
        keys += keys
        i = 0
        for line in text.text:
            encrypted_text.text.append(self.CryptoLine(line, keys[i:i + len(key)]))
            i += self.NumberOfLetters(line)
            i %= len(key)
        return encrypted_text

    def EncryptVarnam(self, text, key_text):
        encrypted_text = Text()
        i = j = l = 0
        key_line = key_text.text[j]
        key_words = key_line.split()
        j += 1
        while i < len(text.text):
            encrypted_line = ""
            line = text.text[i]
            words = line.split()
            for word in words:
                while l >= len(key_words):
                    key_line = key_text.text[j]
                    j += 1
                    key_words = key_line.split()
                    l = 0
                keys = []
                key_words[l] = key_words[l].lower()
                for letter in key_words[l]:
                    keys.append(ord(letter) - ord('a'))
                encrypted_line += self.CryptoLine(word, keys)
                encrypted_line += " "
                l += 1
            i += 1
            encrypted_line += '\n'
            encrypted_text.text.append(encrypted_line)
        return encrypted_text

class Decryptor(Crypto):
    def DecryptCaesar(self, encrypted_text, key):
        decrypted_text = Text()
        for line in encrypted_text.text:
            decrypted_text.text.append(self.CryptoLine(line, [26 - key]))
        return decrypted_text

    def HackingCaesar(self, encrypted_text):
        frequency = [0.0726, 0.0160, 0.0284, 0.0401, 0.1286, 0.0262, 0.0199, 0.0539,
                     0.0777, 0.0016, 0.0041, 0.0351, 0.0243, 0.0751, 0.0662, 0.0181,
                     0.0017, 0.0683, 0.0662, 0.0972, 0.0248, 0.0115, 0.0180, 0.0017,
                     0.0152, 0.0005]
        number_of_letters = []
        for i in range(26):
            number_of_letters.append(0)
        sum = 0
        for line in encrypted_text.text:
            for letter in line:
                if self.IsBigLetter(letter):
                    number_of_letters[ord(letter) - ord('A')] += 1
                    sum += 1
                elif self.IsSmallLetter(letter):
                    number_of_letters[ord(letter) - ord('a')] += 1
                    sum += 1
        current_frequency = []
        for i in range(26):
            current_frequency.append(number_of_letters[i] / sum)
        i_min = 0
        minim = 2.0
        for i in range(26):
            current_sums = 0.0
            for j in range(26):
                current_sums += (frequency[j] - current_frequency[(j + i) % 26]) ** 2
            if current_sums < minim:
                minim = current_sums
                i_min = i
        return self.DecryptCaesar(encrypted_text, i_min)

    def DecryptVisenere(self, encrypted_text, key):
        decrypted_text = Text()
        keys = []
        key = key.lower()
        for letter in key:
            keys.append(26 - ord(letter) + ord('a'))
        keys += keys
        i = 0
        for line in encrypted_text.text:
            decrypted_text.append(self.CryptoLine(line, keys[i:i + len(key)]))
            i += self.NumberOfLetters(line)
            i %= len(key)
        return decrypted_text

    def DecryptVarnam(self, encrypted_text, key_text):
        decrypted_text = Text()
        i = j = l = 0
        key_line = key_text.text[j]
        key_words = key_line.split()
        j += 1
        while i < len(encrypted_text.text):
            decrypted_line = ""
            line = encrypted_text.text[i]
            words = line.split()
            for word in words:
                while l >= len(key_words):
                    key_line = key_text.text[j]
                    j += 1
                    key_words = key_line.split()
                    l = 0
                keys = []
                key_words[l] = key_words[l].lower()
                for letter in key_words[l]:
                    keys.append(26 - ord(letter) + ord('a'))
                decrypted_line += self.CryptoLine(word, keys)
                decrypted_line += " "
                l += 1
            i += 1
            decrypted_line += '\n'
            decrypted_text.text.append(decrypted_line)
        return decrypted_text


informer = argparse.ArgumentParser(description='Information for encryption.')

informer.add_argument('--action', type=str)
informer.add_argument('--in_path', type=str)
informer.add_argument('--out_path', type=str)
informer.add_argument('--cipher_name', type=str)
informer.add_argument('--key_path', type=str)

info = informer.parse_args()
f = open(info.in_path, 'r')
g = open(info.out_path, 'w')
try:
    k = open(info.key_path, 'r')
except:
    if info.action == "Encrypt":
        g.write("No key is found, cannot encrypt text")
        sys.exit(0)
text = Text(f)

if info.action == "Encrypt":
    en = Encryptor()
    if info.cipher_name == "Caesar":
        key = int(k.read())
        result = en.EncryptCaesar(text, key)
        for line in result.text:
            g.write(line)
    elif info.cipher_name == "Vigenere":
        key = k.read()
        result = en.EncryptVigenere(text, key)
        for line in result.text:
            g.write(line)
    elif info.cipher_name == "Varnam":
        key = Text(k)
        result = en.EncryptVarnam(text, key)
        for line in result.text:
            g.write(line)
    else:
        g.write("Cipther is not recognised")
elif info.action == "Decrypt":
    de = Decryptor()
    if info.cipher_name == "Caesar":
        result = Text()
        try:
            key = int(k.read())
            result = de.DecryptCaesar(text, key)
        except:
            result = de.HackingCaesar(text)
        for line in result.text:
            g.write(line)
    elif info.cipher_name == "Vigenere":
        key = k.read()
        result = de.DecryptVigenere(text, key)
        for line in result.text:
            g.write(line)
    elif info.cipher_name == "Varnam":
        key = Text(key)
        result = de.DecryptVarnam(text, key)
        for line in result.text:
            g.write(line)
    else:
        g.write("Cipther is not recognised")
else:
    g.write("Action can be recognised.")

f.close()
g.close()
try:
    k.close()
except:
    pass
