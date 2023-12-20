import numpy as np

import matplotlib.pyplot as plt


class EvolutionAlgorithm:

    def __init__(self, 
                 profits: list, 
                 constraints: list, 
                 reserves: list, 
                 population_size: int = 1000,
                 bounds: tuple = (0, 1000),
                 num_generations: int = 100,
                 mutation_rate: float = 0.1,
                 tournament_size: int = 10):
        self.profits = profits
        self.constraints = constraints
        self.reserves = reserves
        self.population_size = population_size
        self.bounds = np.array([bounds for _ in range(len(profits))])
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.path = []
        self.solution = {}
        self.genetic_algorithm()
        self.plot()
        

    # Функция для вычисления значения целевой функции
    def objective_function(self, arg: list):
        return np.dot(arg, self.profits)

    # Функция для проверки ограничений
    def in_constraints(self, arg: list):
        return np.all(np.dot(self.constraints, arg) <= self.reserves)

    # Функция для создания начальной популяции
    def initialize_population(self):
        valid_population = []
        num_variables = len(self.profits)
        while len(valid_population) < self.population_size:
            new_individual = np.random.uniform(low=self.bounds[:, 0], high=self.bounds[:, 1], size=num_variables)
            if self.in_constraints(new_individual):
                valid_population.append(new_individual)
        return np.array(valid_population)

    # Функция для выбора особей с использованием турнирного отбора
    def tournament_selection(self, population: list, fitness: list):
        selected_indices = []
        for _ in range(len(population)):
            tournament_indices = np.random.choice(len(population), self.tournament_size, replace=False)
            tournament_fitness = [fitness[i] for i in tournament_indices]
            selected_indices.append(tournament_indices[np.argmax(tournament_fitness)])
        return selected_indices

    # Функция для скрещивания двух родителей
    def crossover(self, parent1: list, parent2: list):
        crossover_point = np.random.randint(1, len(parent1))
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return child

    # Функция для мутации
    def mutate(self, child: list, gen_num: int):
        mutation_mask = np.random.rand(len(child)) < self.mutation_rate
        child[mutation_mask] += np.random.uniform(low=-10 / (gen_num + 1), high=10 / (gen_num + 1), size=np.sum(mutation_mask))
        zero_koef = np.random.uniform(0, 1) < self.mutation_rate
        if zero_koef:
            child[np.random.randint(len(child))] = 0
        return child
    
    def plot(self):
        plt.figure(figsize=(8, 6))
        plt.plot(list(range(1, len(self.path) + 1)), self.path, marker='o', linestyle='-', color='b')

        plt.title('Зависимость максимальных значений в каждой популяции')
        plt.xlabel('Номер популяции (или поколения)')
        plt.ylabel('Максимальное значение')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/images/plot.png")
        plt.close()

    # Генетический алгоритм
    def genetic_algorithm(self):
        population = self.initialize_population()
        self.path.clear()
        print("Initialized!")
        
        best_solution = None
        best_fitness = float('-inf')  # Инициализация с минус бесконечностью
        
        for generation in range(self.num_generations):
            fitness = [self.objective_function(ind) for ind in population]
            
            # Проверка ограничения на лучшие особи
            current_best_index = np.argmax(fitness)
            current_best_fitness = fitness[current_best_index]
            if current_best_fitness > best_fitness:
                best_solution = population[current_best_index]
                best_fitness = current_best_fitness
            self.path.append(best_fitness)

            # Выбор лучших особей с использованием турнирного отбора
            selected_indices = self.tournament_selection(population, fitness)
            selected_population = population[selected_indices]
            
            # Создание новой популяции с использованием скрещивания и мутации
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = selected_population[np.random.choice(len(selected_population), 2, replace=False)]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                child1 = self.mutate(child1, generation)
                child2 = self.mutate(child2, generation)
                if self.in_constraints(child1):
                    new_population.extend([child1])
                if self.in_constraints(child2):
                    new_population.extend([child2])
            
            # Применение границ переменных
            new_population = np.clip(new_population, self.bounds[:, 0], self.bounds[:, 1])
            population = np.array(new_population)

        self.solution = {
            "parameters": best_solution,
            "best_value": best_fitness
        }