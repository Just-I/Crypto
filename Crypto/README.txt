Запуск шифрования/расшифрования файла:

python3 Crypto.py --action=<> --in_path=path_to_input_file/input.txt --out_path=path_to_output_file/output.txt --cipher_name=CipherName --key_path=path_to_key/key.txt

(на место <> либо Encrypt, либо Decrypt)
Пример:

python3 Crypto.py --action=Encrypt --in_path=text.txt --out_path=encrypted.txt --cipher_name=Caesar --key_path=key.txt

python3 Crypto.py --action=Decrypt --in_path=encrypted.txt --out_path=decrypted.txt --cipher_name=Caesar --key_path=key.txt

Для взлома зашифрованного шифром Цезаря сообщения, оставьте путь до ключа пустым

Пример:

python3 Crypto.py --action=Decrypt --in_path=encrypted.txt --out_path=decrypted_without_key.txt --cipher_name=Caesar --key_path=

Возможные шифры:
Caesar - шифр Цезаря, ключ - число
Vigenere - шифр Виженера, ключ - строка
Varnam - шифр Варнама, ключ - строки