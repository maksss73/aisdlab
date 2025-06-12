import tkinter as tk
from tkinter import scrolledtext
import itertools

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор комбинаций")
        self.root.configure(bg='#746363')

        tk.Label(root, text="Введите N (положительное число):", background='#a58888').grid(row=0, column=0, sticky="w", padx=10, pady=5,)
        self.entry_N = tk.Entry(root, background='#a58888')
        self.entry_N.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Введите K (положительное число):", background='#a58888').grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_K = tk.Entry(root, background='#a58888')
        self.entry_K.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Введите бюджет:", background='#a58888').grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_budget = tk.Entry(root, background='#a58888')
        self.entry_budget.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Введите цены через запятую:", background='#a58888').grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_costs = tk.Entry(root, background='#a58888')
        self.entry_costs.grid(row=3, column=1, padx=10, pady=5)

        self.button = tk.Button(root, text="Вычислить", command=self.run_algorithm, background='#a58888')
        self.button.grid(row=4, column=0, columnspan=2, pady=10)

        self.output_text = scrolledtext.ScrolledText(root, width=60, height=10, background='#9e8f8f')
        self.output_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def algoritm(self, N, K):
        options = list(range(N)) + [None]
        return list(itertools.product(options, repeat=K))

    def limit_approach(self, N, K, costs, budget, result_algo):
        variants = []
        for choice in result_algo:
            selected = [i for i in choice if i is not None]
            total_cost = sum(costs[i] for i in selected)
            if total_cost <= budget:
                variants.append(choice)
        return variants

    def run_algorithm(self):
        try:
            N = int(self.entry_N.get())
            K = int(self.entry_K.get())
            budget = int(self.entry_budget.get())
            costs = list(map(int, self.entry_costs.get().split(',')))
            assert N > 0 and K > 0, "N и K должны быть положительными"
            assert len(costs) == N, "Количество цен должно совпадать с N"

            result_algo = self.algoritm(N, K)
            result_limited = self.limit_approach(N, K, costs, budget, result_algo)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Общее количество вариантов: {len(set(result_limited))}\n\n")
            for variant in result_limited:
                self.output_text.insert(tk.END, f"{variant}\n")
        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Ошибка: {str(e)}")


root = tk.Tk()
app = App(root)
root.mainloop()
