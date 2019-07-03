from path_finding import PathFinding, distance
from random import randint, uniform
import math
from decimal import Decimal



def xy_current(x, y):
    global xx, yy
    xx = x
    yy = y


class Genetic_Algorithm(PathFinding):
    def __init__(self, chromosome_length, population_size, generation_gap, mutation_rate, elitism, sel_criteria):
        self.grid = []
        self.patients = None
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.generation_gap = generation_gap
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.selection_criteria = sel_criteria
        self.init_grid()
    # the chromosome length is 5, which means that all possible nodes cannot be a part of the chromosome.
    # the 5 genes of a chromosome, each represent points that are path of the path between the start node and goal node.
    # fist node is start node, the last node is the goal node, and the three genes in the middle are intermediate nodes.
    #creates a single chromosome
    def create_single_chromosome(self):
        c = [[self.start.r, self.start.c]]
        c.extend([[randint(0, self.grid_rows - 1), randint(0, self.grid_cols - 1)] for x in
                  range(self.chromosome_length)])
        c.append([self.goal.r, self.goal.c])
        return c
    #creates chromosomes equal to population_size
    def create_chromosomes(self):
        self.chromosomes = [self.create_single_chromosome() for i in range(self.population_size)]

    #we assume a direct path - line between each of the 5 nodes.
    def chromosome_path(self, chromosome):
        temp_path = [chromosome[0]]
        for i in range(0, len(chromosome) - 1):
            xy_current(chromosome[i][0], chromosome[i][1])
            while ([xx, yy] != chromosome[i + 1]):
                if (xx != chromosome[i + 1][0]):
                    if (xx < chromosome[i + 1][0]):
                        xy_current(xx + 1, yy)
                    else:
                        xy_current(xx - 1, yy)

                if (yy != chromosome[i + 1][1]):
                    if (yy < chromosome[i + 1][1]):
                        xy_current(xx, yy + 1)
                    else:
                        xy_current(xx, yy - 1)
                temp_path.append((xx, yy))
        return temp_path
    #the fitness function evaluates fitness of each chromosome
    def fitness(self, chromosome):
        complete_path = [self.get(pair[0], pair[1]) for pair in self.chromosome_path(chromosome)]
        distances = 0
        blocks = 0
        for i in range(0, len(complete_path) - 1):
            distances += distance(complete_path[i], complete_path[i + 1])
            if (complete_path[i].reachable == False):
                blocks += 1
        if (complete_path[(len(complete_path) - 1)].reachable == False):
            blocks += 1
        fitness = Decimal(50000 - Decimal(distances ** 2) - Decimal(100000 ** blocks))
        return fitness
    #randomly chooses one-point or two point crossover, betweeen 2 chromosomes, to create 2 new offspring
    def crossover(self, c1, c2):
        if (randint(0, 2)):
            c1, c2 = self.single_point_crossover(c1, c2)
        else:
            c1, c2 = self.two_point_crossover(c1, c2)
        return c1, c2
    #crossover at one point in the chromosome
    def single_point_crossover(self, oc1, oc2):
        c1 = oc1[:]
        c2 = oc2[:]
        a = randint(1, self.chromosome_length)
        b = c1[a:]
        c1[a:] = c2[a:]
        c2[a:] = b[:]
        return c1, c2
    # crossover at two points in the chromosome
    def two_point_crossover(self, oc1, oc2):
        c1 = oc1[:]
        c2 = oc2[:]
        a = randint(1, self.chromosome_length)
        o = randint(1, self.chromosome_length)
        while (a == o):
            o = randint(1, self.chromosome_length)
        if (a < o):
            d = c1[a:o]
            c1[a:o] = c2[a:o]
            c2[a:o] = d[:]
        else:
            a, o = o, a
            d = c1[a:o]
            c1[a:o] = c2[a:o]
            c2[a:o] = d[:]
        return c1, c2

    #multiple crossovers occur among many chromosome
    def multiple_crossovers(self, chromosomes):
        offspring = []
        while (len(chromosomes)):
            a = randint(0, len(chromosomes) - 1)
            b = randint(0, len(chromosomes) - 1)
            while (a == b):
                b = randint(0, len(chromosomes) - 1)
            c1 = chromosomes[a]
            c2 = chromosomes[b]
            chromosomes.remove(c1)
            chromosomes.remove(c2)
            c1, c2 = self.crossover(c1, c2)
            offspring.extend([c1, c2])
        return offspring
    #proportionate selection method is used to select the chromosomes for the next iteration
    #a chromosome's probability of getting selected is equal to its fitness in proportion to
    #the total fitness of all the chromosomes
    def proportionate_selection(self, chromosomes_fitness, to_be_replaced):
        offspring = []
        total = Decimal('0.0')
        for a in chromosomes_fitness:
            total += a[1]
        # total = sum([a[1] for a in chromosomes_fitness])
        proportion = []
        for a in chromosomes_fitness:
            proportion.append((a[1] / total))
        #        proportion = [(a[1]/total)*100 for a in chromosomes_fitness]
        sections = []
        for i in range(0, len(proportion)):
            x = (self.population_size - (i + 1)) * (proportion[-1] - proportion[0]) / (
                        self.population_size - 1) + proportion[0]
            sections.append(x)
        #        sections = [sum(proportion[:i+1]) for i in range(0, len(proportion))]
        for i in range(int(math.floor(to_be_replaced / 2))):
            choice1 = uniform(0, 100)
            choice2 = uniform(0, 100)
            while (choice1 == choice2):
                choice2 = uniform(0, 100)
            for i in range(0, len(sections)):
                if ((sections[i] > choice1)):
                    for j in range(0, len(sections)):
                        if ((sections[j] > choice2)):
                            c1 = chromosomes_fitness[i - 1][0][:]
                            c2 = chromosomes_fitness[j - 1][0][:]
                            c1, c2 = self.crossover(c1, c2)
                            offspring.extend([c1, c2])
        return offspring
    #random sudden changes in a chromosome's genes
    def mutation(self, ochromosome):
        chromosome = ochromosome[:]
        while (True):
            a = [randint(1, self.grid_rows - 1), randint(1, self.grid_cols - 1)]
            if (self.get(a[0], a[1]).reachable):
                break
        chromosome[randint(2, self.chromosome_length) - 1] = a
        return chromosome
    #many chromosomes are mutated
    def mutate_many(self, chromosomes):
        mutated = []
        for c in chromosomes:
            c = self.mutation(c)
            mutated.append(c)
        return mutated
    #fitness of the whole population is calculated
    def compute_all_fitnesses(self):
        all_chromosome_fitness = [(chromosome, self.fitness(chromosome)) for chromosome in self.chromosomes]
        self.all_chromosome_fitness = sorted(all_chromosome_fitness, key=lambda tup: tup[1], reverse=True)
    #rate of utation increased
    def increase_mutation(self):
        self.mutation_rate = self.mutation_rate * 2
        if (self.mutation_rate > 0.4):
            self.mutation_rate = 0.4
    #duplicate chromosomes removed
    def remove_duplicate(self, mylist):
        newlist = []
        for item_tuple in mylist:
            exists = False
            for every_element in newlist:
                if item_tuple[0] == every_element[0] and item_tuple[1] == every_element[1]:
                    exists = True
            if (exists == False):
                newlist.append(item_tuple)
        return newlist
    #the path for the ambulance is determined
    def node_path(self, chromosome):
        chromosome_path = self.chromosome_path(chromosome)
        optimal_path = []
        for xy in chromosome_path:
            optimal_path.append(self.get(xy[0], xy[1]))
        return optimal_path
    #implementation of the algorithm
    def genetic_algorithm(self, iterations):
        self.create_chromosomes()
        elite_total = int(self.elitism * self.population_size)
        to_be_replaced_total = int(self.generation_gap * self.population_size)
        if (to_be_replaced_total % 2 == 1):
            to_be_replaced_total += 1
        to_be_mutated_total = int(self.mutation_rate * self.population_size)
        offspring = []
        count = 0
        max_fitness_previous = 0
        for j in range(iterations):
            self.compute_all_fitnesses()

            self.all_chromosome_fitness = self.remove_duplicate(self.all_chromosome_fitness)[:]
            self.chromosomes = []
            if (max_fitness_previous == self.all_chromosome_fitness[0][1]):
                count += 1
                if (count == 4):
                    count = 0
            elite_chromosomes = [self.all_chromosome_fitness[i][0] for i in range(elite_total)]
            if (self.selection_criteria == 'proportionate'):
                offspring = self.proportionate_selection(self.all_chromosome_fitness, to_be_replaced_total)
            # offspring = self.multiple_crossovers([self.all_chromosome_fitness[i][0] for i in range(to_be_replaced_total)])
            mutated = self.mutate_many(
                [self.all_chromosome_fitness[i][0] for i in range((to_be_mutated_total))])
            self.chromosomes.extend(elite_chromosomes)

            self.chromosomes.extend(offspring)
            self.chromosomes.extend(mutated)
            self.chromosomes = self.chromosomes[:self.population_size]

            max_fitness_previous = self.all_chromosome_fitness[0][1]
            print('iter:', j, 'pop_size:', len(self.chromosomes), 'max fitness:',
                  self.all_chromosome_fitness[0][1])

        optimal_path = self.node_path(self.all_chromosome_fitness[0][0])
        self.plot_path(optimal_path)

#this is the line for GA
finding = Genetic_Algorithm(chromosome_length=5, population_size=30, generation_gap=0.5, mutation_rate=0.2, elitism=0.3, sel_criteria='proportionate')
#algorithm runs for 200 iterations
finding.genetic_algorithm(200)
