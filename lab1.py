words1 = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре',5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}
def num2words(num):
    return ' '.join(words1[int(digit)] for digit in str(num))
with open('input.txt', 'r') as f:
    for line in f:
        for word in line.split():
            if word.isdigit():
                if len(word) > 1 and word.startswith('000'):  # ≥3 нуля
                    number = word.lstrip('0') or '0'  # Удаляем нули, но оставляем "0" если всё нули
                    print(number)
                    seen_digits = []
                    for digit in word:
                        if digit not in seen_digits:
                            seen_digits.append(digit)
                    print(' '.join(words1[int(digit)] for digit in seen_digits))
