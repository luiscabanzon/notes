def load_items(file):
	item_list = []
	f = open(file).readlines()
	for line in f:
		item_list.append(line.split())
	item_list = sorted(item_list, key= lambda x: float(x[1])/float(x[2]), reverse=True)
	return item_list

items = load_items('item_list.txt')
print(items)

def random_solution(n_genes, seed):
	from random import choice
	solution = []
	for i in range(n_genes):
		solution.append(choice([0,1]))
	return solution

def fitness(solution, ref_list, backpack_capacity):
	fitness_score = 0
	total_weight = 0
	for i in range(len(solution)):
		gene = solution[i]
		weigth = float(ref_list[i][2])
		total_weight += weigth * gene
		#print(total_weight)

		if total_weight > backpack_capacity:
			return fitness_score

		value = float(ref_list[i][1])
		fitness_score += gene * (value/weigth)
	return fitness_score

def create_population(size,element_generator,n_genes, seed):
	population = []
	for i in range(size):
		population.append(element_generator(n_genes, seed))
	return population

def termination_condition():
	pass



def tournament_selector(population,n_selections,fitness_function,tournament_size=2,choose_fittest=1,replacement=False):
	from random import sample, uniform
	pop_index = list(range(len(population)))
	selected_solutions = []
	n_selected = 0
	for i in range(n_selections):
		candidates = [population[e] for e in sample(pop_index, tournament_size)]
		#DELETE
		print candidates
		print map(lambda x: sum(x), candidates)
		sorted_candidates = sorted(candidates, key= lambda x: fitness_function(x, items, 65), reverse=True)
		winner = False
		for j in sorted_candidates:
			if uniform(0,1) <= choose_fittest:
				winner = j
				break
		if not winner:
			winner = sorted_candidates[-1]
		selected_solutions.append(winner)
		if replacement == False:
			candidates.remove(winner)
		#DELETE
		print sum(winner)
	return selected_solutions

#################
# TEST
#################
population = create_population(100,random_solution, len(items), 42)
print(population)

print(fitness([0,1,1,0,0,1,0], items, 100)) # = 7

print(fitness([1,1,1,0,0,0,0], items, 100)) # = 4.5

print(fitness([1,1,1,1,1,1,1], items, 100)) # = 4.5

new_population = tournament_selector(population, 5, fitness)
print(new_population)