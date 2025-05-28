import time
import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal, getcontext

getcontext().prec = 50

# Факториал
def factorial(n):
    result = Decimal(1)
    for i in range(1, n + 1):
        result *= i
    return result

# Рекурсивные F и G
def F_recursive(n):
    if n == 1:
        return 1
    return (-1) ** n * (2 * F_recursive(n - 1) - G_recursive(n - 1))

def G_recursive(n):
    if n == 1:
        return 1
    F_prev, G_prev = F_recursive(n - 1), G_recursive(n - 1)
    return 2 * F_prev / (factorial(2 * n)) + G_prev

# Итерационные F и G
def FG_iterative(n):
    F, G = [0] * (n + 1), [0] * (n + 1)
    F[1], G[1] = 1, 1
    for i in range(2, n + 1):
        F[i] = (-1) ** i * (2 * F[i - 1] - G[i - 1])
        G[i] = 2 * F[i - 1] / (factorial(2 * i)) + G[i - 1]
    return F[n], G[n]

# Сравнение времени
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
        times['F_iter'].append(time.perf_counter() - start)
        FG_iterative(n)[0]
        
        start = time.perf_counter()
        try:
            G_recursive(n)
            times['G_rec'].append(time.perf_counter() - start)
        except RecursionError:
            times['G_rec'].append(float('inf'))
            
        start = time.perf_counter()
        times['G_iter'].append(time.perf_counter() - start)
        FG_iterative(n)[1]
    
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

# Основная программа
def main():
    max_n = 10
    df = measure_time(max_n)
    print("\nВремя выполнения:")
    print(df)
    df.to_csv('times.csv', index=False)
    plot_times(df)

if __name__ == "__main__":
    main()
