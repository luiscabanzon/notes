# -*- coding: utf-8 -*-
__author__ = 'Luis Cabanzón'

from random import choice, sample, uniform

def load_items(file):
    item_list = []
    f = open(file).readlines()
    for line in f:
        item = dict()
        item['value'] = float(line[0])
        item['weight'] = float(line[1])
        item_list.append(item)
    item_list = sorted(item_list, key=lambda x: x['value'] / x['weight'], reverse=True)
    return item_list

items = load_items('item_list_2.txt')

def random_solution(n_genes):
    solution = []
    for i in range(n_genes):
        solution.append(choice([0, 1]))
    return solution


def fitness(solution, ref_list, backpack_capacity):
    fitness_score = 0
    total_weight = 0
    for i in range(len(solution)):
        gene = solution[i]
        weight = float(ref_list[i]['weight'])
        total_weight += weight * gene
        # print(total_weight)

        if total_weight > backpack_capacity:
            return fitness_score

        value = float(ref_list[i]['value'])
        fitness_score += gene * (value / weight)
    return fitness_score


def create_population(size, element_generator, n_genes):
    population = []
    for i in range(size):
        population.append(element_generator(n_genes))
    return population


def termination_condition():
    pass


def tournament_selector(population, n_selections, fitness_function,
                        tournament_size=2, choose_fittest=1):
    pop_index = list(range(len(population)))
    selected_solutions = []

    for i in range(n_selections):
        candidates = [population[e] for e in sample(pop_index, tournament_size)]
        # DELETE
        #print candidates
        #print map(lambda x: sum(x), candidates)
        sorted_candidates = sorted(candidates, key=lambda x: fitness_function(x, items, 65), reverse=True)
        winner = False
        for j in sorted_candidates:
            if uniform(0, 1) <= choose_fittest:
                winner = j
                break
        if not winner:
            winner = sorted_candidates[-1]
        selected_solutions.append(winner)
        # DELETE
        #print sum(winner)
    return selected_solutions


def onepoint_crossover(parent_A, parent_B, crossover_rate=0.5):
	# print parent_A, parent_B
	parent_size = len(parent_A)
	onepoint = choice(range(parent_size))
	# print onepoint
	if uniform(0, 1) <= crossover_rate:
		children_A = parent_A[0:onepoint] + parent_B[onepoint:]
		children_B = parent_B[0:onepoint] + parent_A[onepoint:]
	else:
		children_A = parent_A
		children_B = parent_B
	# print children_A, children_B
	return [children_A, children_B]


def mutate(solution, mutation_rate=1.0 / len(items)):
	return [pow(1, x) if uniform(0, 1) <= mutation_rate else x for x in solution]


def evaluate_population(population, fitness_function, items, backpack_capacity):
	# print type(population)
	# print len(population)
	return sum([fitness_function(solution, items, backpack_capacity) for solution in population]) / float(len(population))

#################
# TEST
#################

print(items)
population = create_population(100, random_solution, len(items))
'''
print(population)

print(fitness([0, 1, 1, 0, 0, 1, 0], items, 100))  # = 7

print(fitness([1, 1, 1, 0, 0, 0, 0], items, 100))  # = 4.5

print(fitness([1, 1, 1, 1, 1, 1, 1], items, 100))  # = 4.5

new_population = tournament_selector(population, 100, fitness)
print(new_population)

print(onepoint_crossover([1, 1, 1, 1, 1], [0, 0, 0, 0, 0], 1))
print(onepoint_crossover([1, 1, 1, 1, 1], [0, 0, 0, 0, 0], 0))

print(map(lambda x: mutate(x), new_population))

print(evaluate_population(new_population, fitness, items, 100))
'''
performance = []
for R in range(100):
	new_population = tournament_selector(population, 100, fitness)
	parents_A = new_population[:int(len(new_population) / 2)]
	parents_B = new_population[int(len(new_population) / 2):]
	children = []
	for p in range(len(parents_A) - 1):
		children += onepoint_crossover(parents_A[p], parents_B[p], 0.5)
	mutated_children = [mutate(child) for child in children]
	best_solution = sorted(new_population, key=lambda x: fitness(x, items, 100), reverse=True)[0]
	# print "Best Solution: %s" % best_solution
	population = mutated_children + [best_solution]
	#print len(population)
	# print population
	print("Generation %s. Avg. Score: %s" % (R, evaluate_population(population, fitness, items, 100)))
	#performance.append(evaluate_population(population, fitness, items, 100))

best_solution = sorted(new_population, key=lambda x: fitness(x, items, 100), reverse=True)[0]
print "Best Solution: %s" % best_solution
#for p in performance:
	# print p