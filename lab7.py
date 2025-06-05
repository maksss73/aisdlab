import time
import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal, getcontext
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading #многопоточность

getcontext().prec = 50

def factorial(n):
    result = Decimal(1)
    for i in range(1, n + 1):
        result *= i
    return result
def F_recursive(n):
    if n == 1:
        return 1
    return (-1) ** n * (2 * F_recursive(n - 1) - G_recursive(n - 1))
def G_recursive(n):
    if n == 1:
        return 1
    F_prev, G_prev = F_recursive(n - 1), G_recursive(n - 1)
    return 2 * F_prev / (factorial(2 * n)) + G_prev


def FG_iterative(n):
    F, G = [0] * (n + 1), [0] * (n + 1)
    F[1], G[1] = 1, 1
    for i in range(2, n + 1):
        F[i] = (-1) ** i * (2 * F[i - 1] - G[i - 1])
        G[i] = 2 * F[i - 1] / (factorial(2 * i)) + G[i - 1]
    return F[n], G[n]


def measure_time(max_n):
    times = {'n': [], 'F_rec': [], 'F_iter': [], 'G_rec': [], 'G_iter': []}
    for n in range(1, max_n + 1):
        times['n'].append(n)

        start = time.perf_counter()
        try:
            F_recursive(n)
            times['F_rec'].append(time.perf_counter() - start)
        except RecursionError:
            times['F_rec'].append(float('inf'))

        start = time.perf_counter()
        FG_iterative(n)[0]
        times['F_iter'].append(time.perf_counter() - start)

        start = time.perf_counter()
        try:
            G_recursive(n)
            times['G_rec'].append(time.perf_counter() - start)
        except RecursionError:
            times['G_rec'].append(float('inf'))

        start = time.perf_counter()
        FG_iterative(n)[1]
        times['G_iter'].append(time.perf_counter() - start)

    return pd.DataFrame(times)


# Графики
def plot_times(df):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(df['n'], df['F_rec'], 'o-', label='F Recursive')
    plt.plot(df['n'], df['F_iter'], 'x-', label='F Iterative')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.title('F(n)')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(df['n'], df['G_rec'], 'o-', label='G Recursive')
    plt.plot(df['n'], df['G_iter'], 'x-', label='G Iterative')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.title('G(n)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('times.png')
    plt.show()


# результаты
def compute_and_display():
    try:
        max_n = int(entry_max_n.get())
        if max_n <= 0:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Ошибка: Введите положительное число.\n")
            return
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите корректное число.\n")
        return

    df = measure_time(max_n)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Время выполнения:\n")
    output_text.insert(tk.END, df.to_string() + "\n")

    df.to_csv('times.csv', index=False)

    # графики в отдельном потоке
    threading.Thread(target=plot_times, args=(df,), daemon=True).start()


#GUI
root = tk.Tk()
root.title("Сравнение времени выполнения F(n) и G(n)")
root.geometry("600x400")

label_instruction = tk.Label(root, text="Введите max_n для вычисления времени выполнения функций F(n) и G(n):")
label_instruction.pack(pady=5)


entry_max_n = tk.Entry(root, width=10)
entry_max_n.pack(pady=5)
entry_max_n.insert(0, "7")

btn_compute = tk.Button(root, text="Вычислить", command=compute_and_display)#Кнопка
btn_compute.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)#Поле вывода с прокруткой
output_text.pack(pady=10)


root.mainloop()
