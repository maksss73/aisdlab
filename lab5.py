import itertools

# Молодые (18-30 лет): 1, 3, 5, 7, 9; Старшие (31+): 2, 4, 6, 8, 10
young = [1, 3, 5, 7, 9]
older = [2, 4, 6, 8, 10]

def team_strength(team):
    """Считаем силу команды как произведение номеров сотрудников."""
    young_emp, older_emp = team
    return young_emp * older_emp

def is_valid_team(team):
    """Проверяем ограничение: разница между номерами >= 3."""
    young_emp, older_emp = team
    return abs(young_emp - older_emp) >= 3

def total_strength(distribution):
    """Считаем общую силу распределения как сумму сил всех команд."""
    return sum(team_strength(team) for team in distribution)

def distribute_employees():
    valid_distributions = []  # Список для хранения всех допустимых вариантов

    # Генерируем все перестановки старших сотрудников
    for perm in itertools.permutations(older):
        # Формируем команды, соединяя молодых и старших
        teams = list(zip(young, perm))
        # Проверяем, что все команды удовлетворяют ограничению
        if all(is_valid_team(team) for team in teams):
            valid_distributions.append((teams, total_strength(teams)))
    
    # Сортируем по убыванию общей силы и возвращаем только распределения
    return [dist for dist, _ in sorted(valid_distributions, key=lambda x: x[1], reverse=True)]

# Подсчитываем общее количество возможных комбинаций без учета ограничений
total = 1
for i in range(1, len(older) + 1):
    total *= i
print(f"Всего возможных комбинаций без учета ограничений: {total}")

# Находим и выводим оптимальные варианты
distributions = distribute_employees()
print(f"Количество допустимых комбинаций с учетом ограничений: {len(distributions)}\n")
for i, distribution in enumerate(distributions, 1):
    print(f"Комбинация {i} (сила = {total_strength(distribution)}): {distribution}")

# Выводим лучший вариант
if distributions:
    best_distribution = distributions[0]
    print(f"\nОптимальная комбинация (максимальная сила = {total_strength(best_distribution)}): {best_distribution}")
else:
    print("Нет допустимых распределений с учетом ограничений.")
