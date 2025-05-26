import re
WORDS = {'0': "ноль", '1': "один", '2': "два", '3': "три", '4': "четыре", '5': "пять", '6': "шесть", '7': "семь",
         '8': "восемь", '9': "девять"}
with open("input.txt", 'r', encoding='utf-8') as file:
    t = file.read()
    pattern = r'\b0{3,}\d+\b'
    match = re.findall(pattern, t)
    for m in match:
        number = m.lstrip('0')
        print(number if number else '0')
        Digits = sorted(set(number))
        print("Использованные цифры:", ", ".join(WORDS[d] for d in Digits))
