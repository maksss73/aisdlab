# Задача: распределить премию между бригадой
# Вариант 24

import time
import itertools

# 1 часть - два способа распределения премии

# Способ 1 - алгоритмический (ручной перебор)
def manual_distribution(people_count, bonus_total):
    """
    Ручной способ - сам все перебираю
    """
    all_variants = []
    
    # Вспомогательная функция для рекурсии
    def find_variants(people_left, money_left, current_variant):
        # Если дошли до последнего человека
        if people_left == 1:
            # Отдаем все оставшиеся деньги последнему
            final = current_variant + [money_left]
            all_variants.append(final)
            return
        
        # Перебираем сколько дать текущему человеку с шагом 1000 рублей
        for money in range(0, money_left + 1, 1000):
            find_variants(people_left - 1, 
                         money_left - money, 
                         current_variant + [money])
    
    find_variants(people_count, bonus_total, [])
    return all_variants

# Способ 2 - питоновский (используем готовые функции)
def python_distribution(people_count, bonus_total):
    """
    Питоновский способ - использую itertools с шагом
    """
    variants = []
    
    # Генерируем возможные суммы с шагом 1000 рублей
    possible_amounts = list(range(0, bonus_total + 1, 1000))
    
    # Генерируем комбинации
    for combo in itertools.combinations_with_replacement(possible_amounts, people_count):
        if sum(combo) == bonus_total:
            variants.append(list(combo))
    
    return variants

# Сравниваем время работы двух способов
def compare_methods():
    people = 3
    bonus = 50000  # Реальная премия - 50 000 рублей
    
    print(f"Бригада: {people} чел, Премия: {bonus:,} руб".replace(',', ' '))
    print("=" * 40)
    
    # Замеряем время для ручного способа
    start = time.time()
    manual_result = manual_distribution(people, bonus)
    manual_time = time.time() - start
    
    # Замеряем время для питоновского способа
    start = time.time()
    python_result = python_distribution(people, bonus)
    python_time = time.time() - start
    
    print(f"Ручной способ: {len(manual_result)} вариантов, время: {manual_time:.4f} сек")
    print(f"Питоновский способ: {len(python_result)} вариантов, время: {python_time:.4f} сек")
    
    # Показываем несколько примеров
    print("\nПримеры распределений:")
    for i, variant in enumerate(manual_result[:5]):
        formatted_variant = [f"{x:,}".replace(',', ' ') for x in variant]
        print(f"Вариант {i+1}: {formatted_variant}")

# 2 часть - усложняем задачу с ограничениями

def find_optimal(people_count, bonus_total, min_bonus=10000, max_bonus=30000):
    """
    Усложненная версия с ограничениями:
    - мин премия на человека
    - макс премия на человека
    - ищем самый справедливый вариант
    """
    
    def evaluate_fairness(variant):
        """
        Целевая функция: чем меньше разница между макс и мин - тем лучше
        """
        return max(variant) - min(variant)
    
    # Генерируем варианты с ограничениями
    valid_variants = []
    
    def find_with_constraints(people_left, money_left, current_variant):
        # Проверяем ограничения по ходу
        if any(x < min_bonus or x > max_bonus for x in current_variant):
            return  # Не подходит по ограничениям
        
        # Если денег недостаточно для оставшихся людей
        if money_left < min_bonus * people_left:
            return
        
        # Если денег слишком много для оставшихся людей
        if money_left > max_bonus * people_left:
            return
        
        if people_left == 1:
            # Проверяем последнего человека
            if min_bonus <= money_left <= max_bonus:
                final = current_variant + [money_left]
                valid_variants.append(final)
            return
        
        # Перебираем только допустимые суммы с шагом 1000 рублей
        start_money = max(min_bonus, 0)
        end_money = min(money_left, max_bonus)
        
        for money in range(start_money, end_money + 1, 1000):
            find_with_constraints(people_left - 1, 
                                 money_left - money, 
                                 current_variant + [money])
    
    find_with_constraints(people_count, bonus_total, [])
    
    # Ищем самый справедливый вариант
    if valid_variants:
        most_fair = min(valid_variants, key=evaluate_fairness)
        return valid_variants, most_fair
    else:
        return [], None

def run_advanced():
    """
    Запускаем усложненную версию
    """
    people = 4
    bonus = 100000  # Реальная премия - 100 000 рублей
    min_b = 20000   # Минимум 20 000 на человека (реалистичнее)
    max_b = 30000   # Максимум 30 000 на человека
    
    print(f"\nУсложненная версия:")
    print(f"Люди: {people}, Премия: {bonus:,} руб".replace(',', ' '))
    print(f"Ограничения: от {min_b:,} до {max_b:,} на человека".replace(',', ' '))
    print("=" * 60)
    
    start = time.time()
    variants, best = find_optimal(people, bonus, min_b, max_b)
    time_taken = time.time() - start
    
    print(f"Найдено {len(variants)} допустимых вариантов")
    print(f"Время: {time_taken:.4f} сек")
    
    if best is not None:
        print(f"\nСамый справедливый вариант:")
        formatted_best = [f"{x:,}".replace(',', ' ') for x in best]
        print(f"Распределение: {formatted_best}")
        print(f"Разброс: {max(best) - min(best):,} руб".replace(',', ' '))
        print(f"Сумма: {sum(best):,} руб".replace(',', ' '))
        
        # Показываем статистику
        print(f"\nСтатистика:")
        for i, money in enumerate(best):
            print(f"Человек {i+1}: {money:,} руб".replace(',', ' '))
    else:
        print("Нет подходящих вариантов!")
    
    return variants, best

# Главная функция
def main():
    print("РАСПРЕДЕЛЕНИЕ ПРЕМИИ")
    print("=" * 25)
    
    # Часть 1 - два способа
    compare_methods()
    
    # Часть 2 - усложненная
    variants, best = run_advanced()
    
    # Показываем еще пару вариантов для примера
    if variants:
        print(f"\nВарианты:")
        for i, variant in enumerate(variants[:3]):
            formatted_variant = [f"{x:,}".replace(',', ' ') for x in variant]
            spread = max(variant) - min(variant)
            print(f"Вариант {i+1}: {formatted_variant} (разброс: {spread:,} руб)".replace(',', ' '))

# Запускаем программу
if __name__ == "__main__":
    main()
