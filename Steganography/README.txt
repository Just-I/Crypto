Добавление/извлечение информации из png:

python3 Steganography.py --action=<> --img_path=path_to_image/image.png --text_path=path_to_text/text.txt --key_path=path_to_key/key.txt --new_name=NewNameImage.png

Пример:

python3 Steganography.py --action=Encrypt --img_path=image.png --text_path=input.txt --key_path=keys.txt --new_name=NewImage.png
python3 Steganography.py --action=Decrypt --img_path=NewImage.png --text_path=text.txt --key_path=keys.txt --new_name=NewImage.png