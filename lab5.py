#Вариант 13. Фирма закупает К компьютеров. В магазине компьютеры N типов. Сформировать все возможные варианты покупки.
import time
import itertools

N, K = 5, 3
assert N > 0 and K > 0, "N и K должны быть положительными"

def algoritm(N, K):
    options = list(range(N)) + [None]
    return list(itertools.product(options, repeat=K))

start_time = time.time()
result_algo = algoritm(N, K)
end_time = time.time()
print(f"Алгоритмический подход: {len(result_algo)} вариантов, время выполнения: {end_time - start_time} секунд")


def recursive(N, K):
    results = []
    def backtrack(current, position):
        if position == K:
            results.append(tuple(current))
            return
        for choice in list(range(N)) + [None]:
            backtrack(current + [choice], position + 1)
    backtrack([], 0)
    return results

start_time = time.time()
result_rec = recursive(N, K)
end_time = time.time()
print(f"Рекурсивный подход: {len(result_rec)} вариантов, время выполнения: {end_time - start_time} секунд")

costs = [1000, 1500, 750, 424, 1800]
assert len(costs) == N, "Количество цен должно совпадать с N"
budget = 2300

def limit_approach(N, K, costs, budget):
    variants = []
    for combo in range(0, K + 1):
        for choice in result_algo:
            selected = [i for i in choice if i is not None]
            total_cost = sum(costs[i] for i in selected)
            if total_cost <= budget:
                variants.append(choice)
    return variants

start_time = time.time()
result_limited = limit_approach(N, K, costs, budget)
end_time = time.time()
print(f"Подход с ограничениями: {len(result_limited)} вариантов, время выполнения: {end_time - start_time} секунд")
