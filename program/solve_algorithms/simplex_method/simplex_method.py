from copy import deepcopy


class SimplexMethod:

    def __init__(self, materials: list, reserve: list, profit: list):
        self.vars_amount = len(materials[0])

        self.solution = {
            "iterations": [],
            "parameters": {}
        }

        # Формируем симплекс-таблицу
        self.simplex_table = [materials[i] + [0 if var != i else 1 for var in range(len(materials))] for i in range(len(materials))]
        self.basis = [i + self.vars_amount for i in range(len(materials))]
        self.profits = [prof for prof in profit] + [0 for _ in range(len(materials))]
        self.reserve = reserve

        self.deltas = self.recount_deltas()
        self.save_iteration()
        self.solve()

    def recount_deltas(self):
        new_deltas = []
        i = 0
        for j in range(len(self.simplex_table[i])):
            sum = 0
            for i in range(len(self.simplex_table)):
                sum += self.simplex_table[i][j] * self.profits[self.basis[i]]
            sum -= self.profits[j]
            new_deltas.append(sum)
        return new_deltas

    # Возвращает индекс минимального (отрицательного) значения стоимости товара
    def permissive_column(self):
        return self.deltas.index(min(self.deltas))

    # Возвращает индекс минимального отношения запасов к количеству на единицу товара
    def permissive_row(self, min_profit_ind: int):
        min_index = 0
        min_value = float("inf")
        for i in range(len(self.simplex_table)):
            if self.simplex_table[i][min_profit_ind] <= 0:
                continue
            frac = self.reserve[i] / self.simplex_table[i][min_profit_ind]
            if frac < min_value:
                min_index = i
                min_value = frac
        return min_index
    
    # Пересчитывает всю симплекс-таблицу
    def recount_table(self, row_index: int, col_index: int):
        # Изменяем базисные переменные
        self.basis[row_index] = col_index

        # Разрешающий элемент
        permissive_element = self.simplex_table[row_index][col_index]

        # Пересчитывем запасы
        new_reserves = []
        for i, reserve in enumerate(self.reserve):
            if i == row_index:
                new_reserves.append(reserve / self.simplex_table[i][col_index])
            else:
                new_reserves.append(reserve - self.reserve[row_index] / permissive_element * self.simplex_table[i][col_index])
        self.reserve = new_reserves

        # Пересчитываем коэффициенты симплекс-таблицы
        new_simplex_table = [[None for _ in row] for row in self.simplex_table]
        for i in range(len(self.simplex_table)):
            for j in range(len(self.simplex_table[i])):
                if i == row_index:
                    new_simplex_table[i][j] = self.simplex_table[i][j] / permissive_element
                else:
                    new_simplex_table[i][j] = self.simplex_table[i][j] - self.simplex_table[row_index][j] / permissive_element * self.simplex_table[i][col_index]

        self.simplex_table = new_simplex_table
        self.deltas = self.recount_deltas()

    # Значение целевой функции
    def target_function(self):
        return sum([self.profits[bas_ind] * self.reserve[i] for i, bas_ind in enumerate(self.basis)])
    
    # Итерация
    def iteration(self):
        min_delta_column = self.permissive_column()
        min_q_row = self.permissive_row(min_delta_column)
        self.recount_table(min_q_row, min_delta_column)

    # Сохранение данных текущей итерации
    def save_iteration(self):
        self.solution["iterations"].append( 
            {
                "simplex_table": deepcopy(self.simplex_table),
                "basis": deepcopy(self.basis),
                "deltas": deepcopy(self.deltas),
                "reserves": deepcopy(self.reserve),
                "function": self.target_function(),
                "profits": deepcopy(self.profits)
            }
        )

    def save_results(self):
        parameters = {self.basis[i]: self.reserve[i] for i in range(len(self.basis))}
        real_keys = []
        for key in sorted(parameters.keys()):
            if key < self.vars_amount:
                real_keys.append(key)
        parameters = {key: parameters[key] for key in real_keys}
        self.solution["parameters"] = parameters
        self.solution["function"] = self.target_function()

    def solve(self):
        while (any(delta < 0 for delta in self.deltas)):
            self.iteration()
            self.save_iteration()
        self.save_results()
