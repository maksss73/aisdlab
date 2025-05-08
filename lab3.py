# Функция для чтения матрицы из файла
def read_matrix_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    n = int(lines[0])  # Считываем размер матрицы
    matrix = [list(map(int, line.split())) for line in lines[1:n+1]]  # Считываем строки матрицы
    return n, matrix

# Функция для красивого вывода матрицы
def print_matrix(name, m):
    print(f"\n{name}:")
    for row in m:
        print(" ".join(f"{x:4}" for x in row))

# Транспонирование матрицы (поворот по диагонали)
def transpose(m):
    n = len(m)
    return [[m[j][i] for j in range(n)] for i in range(n)]

# Сложение матриц
def add_matrices(a, b):
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]

# Вычитание матриц
def sub_matrices(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]

# Умножение двух квадратных матриц
def mult_matrices(a, b):
    n = len(a)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += a[i][k] * b[k][j]
    return res

# Умножение матрицы на число
def mult_scalar(k, m):
    return [[k * x for x in row] for row in m]

# Копирование матрицы
def copy_matrix(m):
    return [row[:] for row in m]

# Подсчет нулей в нечетных столбцах области 1
def count_zeros_area1(a):
    n = len(a)
    count = 0
    for i in range(n):
        for j in range(n):
            if i < j and i + j > n - 1 and j % 2 == 1:
                if a[i][j] == 0:
                    count += 1
    return count

# Произведение по периметру области 2
def prod_perimeter_area2(a):
    n = len(a)
    prod = 1
    found = False
    for i in range(n):
        for j in range(n):
            if i > j and i + j > n - 1:
                # Проверка, что элемент на периметре области 2
                if (i == n - 1) or (j == 0) or (i == j + 1) or (i + j == n):
                    prod *= a[i][j]
                    found = True
    return prod if found else 0

# Симметричная замена элементов между областью 1 и 3
def swap_area1_area3(f):
    n = len(f)
    for i in range(n):
        for j in range(n):
            if i < j and i + j > n - 1:  # Условие для области 1
                i2, j2 = n - i - 1, n - j - 1  # Зеркальные координаты (область 3)
                if i2 > j2 and i2 + j2 < n - 1:  # Условие для области 3
                    f[i][j], f[i2][j2] = f[i2][j2], f[i][j]

# Несимметричная замена элементов между областью 2 и 3
def swap_area2_area3(f):
    n = len(f)
    for i in range(n):
        for j in range(n):
            if i > j and i + j > n - 1:  # Условие для области 2
                i2, j2 = n - i - 1, n - j - 1  # Зеркальные координаты (область 3)
                if i2 > j2 and i2 + j2 < n - 1:  # Условие для области 3
                    f[i][j], f[i2][j2] = f[i2][j2], f[i][j]

# Главная функция
def main():
    k = int(input("Введите K: "))  # Ввод числа K
    n, a = read_matrix_from_file("matrix.txt")  # Считываем размер и матрицу A из файла
    print_matrix("A", a)

    f = copy_matrix(a)  # Копируем A в F

    # Вычисляем количество нулей в области 1 и произведение по периметру области 2
    zeros = count_zeros_area1(a)
    perimeter_product = prod_perimeter_area2(a)

    print(f"\nКоличество нулей в нечетных столбцах области 1: {zeros}")
    print(f"Произведение по периметру области 2: {perimeter_product}")

    # В зависимости от условия выполняем замену областей
    if zeros > perimeter_product:
        print("\nУсловие: zero_count > prod_perim → симметрично меняем области 1 и 3")
        swap_area1_area3(f)
    else:
        print("\nУсловие: zero_count <= prod_perim → несимметрично меняем области 2 и 3")
        swap_area2_area3(f)

    print_matrix("F", f)

    # Вычисляем выражение: ((K*A^T)*(F+A) - K*F^T)
    at = transpose(a)
    ft = transpose(f)
    print_matrix("A^T", at)
    print_matrix("F^T", ft)

    kat = mult_scalar(k, at)
    f_plus_a = add_matrices(f, a)
    part1 = mult_matrices(kat, f_plus_a)
    kft = mult_scalar(k, ft)
    result = sub_matrices(part1, kft)

    print_matrix("Результат ((K*A^T)*(F+A) - K*F^T)", result)

main()
