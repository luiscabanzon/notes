def load_items(file):
	item_list = []
	f = open(file).readlines()
	for line in f:
		item_list.append(line.split())
	return item_list

items = load_items('item_list.txt')
print(items)

def random_solution(n_genes):
	from random import choice
	solution = []
	for i in range(n_genes):
		solution.append(choice([0,1]))
	return solution

def create_population(size,element_generator,n_genes):
	population = []
	for i in range(size):
		population.append(element_generator(n_genes))
	return population

population = create_population(100,random_solution, len(items))
print(population)