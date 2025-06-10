#Задана рекуррентная функция. 
#Область определения функции – натуральные числа. 
#Написать программу сравнительного вычисления данной функции рекурсивно и итерационно. 
#Определить границы применимости рекурсивного и итерационного подхода. 
#Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде отчета по лабораторной работе.
#13.	F(1) = 1; G(1) = 1; F(n) = (-1)n*( (n–1)! – G(n–1)), G(n) = F(n–1), при n >=2
import timeit
import matplotlib.pyplot as plt
from tabulate import tabulate

def F_and_G_rec(n, factorial=1):
    if n == 1:
        return 1, 1, factorial
    F_prev, G_prev, prev_factorial = F_and_G_rec(n - 1, factorial * (n - 1))
    sign = 1 if n % 2 == 0 else -1
    F_current = sign * (prev_factorial - G_prev)
    G_current = F_prev
    return F_current, G_current, prev_factorial

def iter_F_and_G(n):
    if n == 1:
        return 1, 1
    F_prev, G_prev = 1, 1
    factorial = 1
    for i in range(2, n + 1):
        factorial *= (i - 1)
        sign = 1 if i % 2 == 0 else -1
        F_current = sign * (factorial - G_prev)
        G_current = F_prev
        F_prev, G_prev = F_current, G_current
    return F_prev, G_prev

def measure_time(func, n, repeat=100):
    return timeit.timeit(lambda: func(n), number=repeat) / repeat * 1000


n_start = 1
max_n_rec = 20
max_n_iter = 20
results = []
n_values = range(n_start, max_n_iter + 1)

for n in n_values:
    try:
        if n <= max_n_rec:
            time_rec = measure_time(F_and_G_rec, n)
        else:
            time_rec = None
    except RecursionError:
        time_rec = None

    time_iter = measure_time(iter_F_and_G, n)
    results.append({
        'n': n,
        'time_rec_ms': time_rec,
        'time_iter_ms': time_iter
    })

table = []
for row in results:
    table.append([
        row['n'],
        f"{row['time_rec_ms']:.4f}" if row['time_rec_ms'] is not None else "N/A",
        f"{row['time_iter_ms']:.4f}"
    ])
print(tabulate(table, headers=['n', 'Рекурсия (мс)', 'Итерация (мс)'], tablefmt='grid'))


plt.figure(figsize=(10, 6))
rec_times = [row['time_rec_ms'] if row['time_rec_ms'] is not None else None for row in results]
iter_times = [row['time_iter_ms'] for row in results]

plt.plot(n_values, iter_times, label='Итерационный метод', marker='o')
plt.plot(n_values[:max_n_rec], rec_times[:max_n_rec], label='Рекурсивный метод', marker='s')

plt.xlabel('n')
plt.ylabel('Время выполнения (мс)')
plt.title('Сравнение времени выполнения рекурсивного и итерационного методов')
plt.legend()
plt.grid(True)
plt.show()
