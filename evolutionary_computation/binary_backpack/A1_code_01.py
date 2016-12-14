# -*- coding: utf-8 -*-
__author__ = 'Luis Cabanzón'

from random import choice, sample, uniform
import json


def create_item_list(size, sort_items=True):
    item_list = dict()
    item_list['items'] = []
    if size == 'small':
        item_list['backpack_capacity'] = int(uniform(100, 10000))
        item_list['list_size'] = 100
    elif size == 'big':
        item_list['backpack_capacity'] = int(uniform(10000, 1000000))
        item_list['list_size'] = 10000
    for i in range(item_list['list_size']):
        item_list['items'].append({'value': int(uniform(1, 101)), 'weight': int(uniform(1, 101))})
    if sort_items:
        item_list['items'] = sorted(item_list['items'], key=lambda x: x['value'] / x['weight'], reverse=True)
    print("List Size: %s" % item_list['list_size'])
    print("Backpack capacity: %s" % item_list['backpack_capacity'])
    return item_list


def random_solution(n_genes):
    solution = []
    for i in range(n_genes):
        solution.append(choice([0, 1]))
    return solution


def create_population(size, solution_generator, n_genes):
    # Create a population of N solutions with n binary elements each
    population = []
    for i in range(size):
        population.append(solution_generator(n_genes))
    return population


def fitness(solution, ref_list):
    # Returns a fitness score
    fitness_score = 0
    total_weight = 0
    for i in range(len(solution)):
        gene = solution[i]
        weight = float(ref_list['items'][i]['weight'])
        total_weight += weight * gene

        if total_weight > ref_list['backpack_capacity']:
            return fitness_score

        value = float(ref_list['items'][i]['value'])
        fitness_score += gene * (value / weight)
    return fitness_score


def tournament_selector(population, n_selections, fitness_function,
                        tournament_size=2, choose_fittest=1):
    # Selects K solutions from the population, using the tournament technique
    pop_index = list(range(len(population)))
    selected_solutions = []

    for i in range(n_selections):
        candidates = [population[e] for e in sample(pop_index, tournament_size)]
        sorted_candidates = sorted(candidates, key=lambda x: fitness_function(x, items), reverse=True)
        winner = False
        for j in sorted_candidates:
            if uniform(0, 1) <= choose_fittest:
                winner = j
                break
        if not winner:
            winner = sorted_candidates[-1]
        selected_solutions.append(winner)
    return selected_solutions


def onepoint_crossover(parent_A, parent_B, crossover_rate=0.5):
    # Generates a children from two different parents, using the onepoint crossover technique
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


def mutate(solution, mutation_rate):
    # Receives a solution and returns it back with mutations (or not, depending on the chance rate)
    # Note pow(1,1)
    return [pow(0, x) if uniform(0, 1) <= mutation_rate else x for x in solution]


def evaluate_population(population, fitness_function, items):
    # print type(population)
    # print len(population)
    return sum([fitness_function(solution, items) for solution in population]) / float(len(population))


params = json.loads(open('parameters.json', 'r').read())
items = create_item_list(params['item_list_size'], params['sort_items'])
population = create_population(100, random_solution, items['list_size'])

performance = []
for R in range(params['iterations']):
    new_population = tournament_selector(population, params['population_size'], fitness, tournament_size=params['tournament_size'])
    parents_A = new_population[:int(len(new_population) / 2)]
    parents_B = new_population[int(len(new_population) / 2):]
    children = []
    for p in range(len(parents_A) - 1):
        children += onepoint_crossover(parents_A[p], parents_B[p], params['crossover_rate'])
    mutated_children = [mutate(child, 1.0/len(items['items'])) for child in children]
    best_solution = sorted(new_population, key=lambda x: fitness(x, items), reverse=True)[0]
    population = mutated_children + [best_solution]
    # print len(population)
    # print population
    score = evaluate_population(population, fitness, items)
    print("Generation %s. Avg. Score: %s" % (R, score))
    print "Best Solution (Gen. %s): %s" % (R, best_solution)
    performance.append(score)

best_solution = sorted(new_population, key=lambda x: fitness(x, items), reverse=True)[0]
print "Best Solution: %s" % best_solution
# for p in performance:
# print p
