from random import seed
from random import randint
from random import random

INFINITY = float("inf")

class Genome(object):
    def __init__(self, n_vertices, n_colors, random=True):
        self.fitness = INFINITY
        self.coloring = [None] * n_vertices

        if(random):
            for i in range(0, n_vertices):
                self.coloring[i] = randint(1, n_colors) -1

    @staticmethod
    def from_chromosome(n_vertices, n_colors, chromosome):
        g = Genome(n_vertices, n_colors, False)
        # make a deep copy
        for i in range(0, len(chromosome)):
            g.coloring[i] = chromosome[i]
        return g

class GeneAlg(object):
    def __init__(self, cross, mut, pop, bits, gene, graph):
        self.crossover_rate = cross
        self.mutation_rate = mut
        self.population_size = pop
        # chromosome is list representation of the graph color assignments
        self.chromosome_length = bits
        # gene is max range of colors allowed to be used starting from 0
        self.gene_length = gene
        self.generation = 0
        self.busy = False
        self.fittest_genome = 0
        self.best_fitness_score = INFINITY
        self.genomes = [None] * pop
        self.graph = graph

        # adjacent_colors() became a bottleneck due to appending to a list
        # for every vertex. I assume because list() is implemented with an
        # array, then the array must be allocated when we over step the 
        # capacity. This function is called for every vertex for every genome
        # once for updating the fitness and once for picking a random color.
        # To advoid this, I created this buffer and reuse it for the duration
        # of the program.
        self.used_colors = [False] * gene
        
        # Used to get intersection of colors
        self.all_colors = set(i for i in range(0, gene))

        self.create_start_population()

    def generations(self):
        return self.generation

    def fittest(self):
        return self.fittest_genome

    def coloring(self):
        chromosome = self.genomes[self.fittest_genome].coloring

        coloring_map = {}
        for vertex in range(0, len(chromosome)):
            coloring_map[vertex] = chromosome[vertex]

        return coloring_map

    def n_colors_used(self):
        chromosome = self.genomes[self.fittest_genome].coloring
        color_set = set()

        for vertex in range(0, len(chromosome)):
            color_set.add(chromosome[vertex])
        return len(color_set)


    def chromosome(self):
        genome = self.genomes[self.fittest_genome]
        result = ""
        for i in range(0, len(genome.coloring)):
            result = result + str(genome.coloring[i]) + " "
        return result

    def started(self):
        return self.busy

    def stop(self):
        self.busy = False

    def calculate_fitness(self, chromosome):
        n_colors_used = set()
        for i in range(0, len(chromosome)):
            n_colors_used.add(i)
        return self.graph.count_bad_edges(chromosome)

    def update_fitness_score(self):
        self.fittest_genome = 0
        self.best_fitness_score = INFINITY

        for i in range(0, self.population_size):
            chromosome = self.genomes[i].coloring
            self.genomes[i].fitness = self.calculate_fitness(chromosome)

            if(self.genomes[i].fitness < self.best_fitness_score):
                self.best_fitness_score = self.genomes[i].fitness
                self.fittest_genome = i

            if(self.genomes[i].fitness == 0):
                self.busy = False
            
    def create_start_population(self):
        for i in range(0, self.population_size):
            self.genomes[i] = Genome(self.chromosome_length, self.gene_length)
        
        self.generation = 0
        self.fittest_genome = 0
        self.best_fitness_score = INFINITY

    def run(self):
        self.create_start_population()
        self.busy = True

    def epoch(self):
        # constant defined in paper
        SELECTION_MUTTION_THRESHOLD = 4
        next_gen = [None] * self.population_size
        self.update_fitness_score()
        noobs = 0

        # The paper discusses keeping the population size constant
        # but the psuedo-code does not mention how. So I think I 
        # can either create 2 children to replace the parents. Or
        # I can take the child and the fittest of the 2 parents
        # into the next generation. I will do the latter.

        counter = 0
        chromosome = [None] * self.chromosome_length
        while(noobs < self.population_size):
            if(self.best_fitness_score > SELECTION_MUTTION_THRESHOLD):
                parents = self.parent_selection1()
                crossed_chromosome = self.crossover(parents[0], parents[1], chromosome)
                mutated_chromosome = self.mutation1(crossed_chromosome)
                next_gen[counter] = Genome.from_chromosome(self.chromosome_length, self.gene_length, mutated_chromosome) 
                counter += 1

                parent = self.max_fitness(parents[0], parents[1])
                next_gen[counter] = parent
                counter += 1
            
            else:
                parents = self.parent_selection2()
                crossed_chromosome = self.crossover(parents[0], parents[1], chromosome)
                mutated_chromosome = self.mutation2(crossed_chromosome)
                next_gen[counter] = Genome.from_chromosome(self.chromosome_length, self.gene_length, mutated_chromosome) 
                counter += 1

                parent = self.max_fitness(parents[0], parents[1])
                next_gen[counter] = parent
                counter += 1

            noobs += 2
        self.genomes = next_gen
        self.generation += 1
        print(self.best_fitness_score)

    def max_fitness(self, g1, g2):
        if(g1.fitness < g2.fitness):
            return g1
        return g2

    def parent_selection1(self):
        parents = list()
        # two random chromosomes from population
        g1 = self.genomes[randint(0, self.population_size-1)]
        g2 = self.genomes[randint(0, self.population_size-1)]
        # take the fitter of the two
        parent1 = self.max_fitness(g1, g2)

        # repeat for the second parent
        g3 = self.genomes[randint(0, self.population_size-1)]
        g4 = self.genomes[randint(0, self.population_size-1)]
        parent2 = self.max_fitness(g3, g4)

        parents.append(parent1)
        parents.append(parent2)
        return parents

        
    def parent_selection2(self):
        # get the top two performers
        first = 0
        second = 0
        best_so_far = INFINITY
        for i in range(0, self.population_size):
            if(self.genomes[i].fitness < best_so_far):
                best_so_far = self.genomes[i].fitness
                second = first
                first = i

        parents = list()
        g1 = self.genomes[first]
        g2 = self.genomes[second]

        parents.append(g1)
        parents.append(g2)
        return parents

    # Given a vertex, check to see if any of the 
    # adjacent verticies have the same color
    def has_adjacent_color(self, vertex, coloring):
        neighbors = self.graph.neighbors_of(vertex)
        for edge in neighbors:
            if(coloring[edge.source] == coloring[edge.target]):
                return True
        return False

    # Given a vertex, return a list of all colors
    # of adjacent verticies.

    def adjacent_colors(self, vertex, coloring):
        neighbors = self.graph.neighbors_of(vertex)

        for edge in neighbors:
            if(coloring[edge.source] == coloring[edge.target]):
                self.used_colors[coloring[edge.target]] = True

    def reset_used_colors(self):
        for i in range(0, len(self.used_colors)):
            self.used_colors[i] = False

    def available_colors(self):
        diff = set()
        for color in range(0, len(self.used_colors)):
            if(self.used_colors[color] == False):
                diff.add(color)
        return list(diff)

    def mutation1(self, chromosome):
        if(random() > self.mutation_rate):
            return chromosome

        coloring = chromosome

        # for each vertex in the chromosome
        for vertex in range(0, len(chromosome)):
            # if the vertex color has the same color as 
            # adjacent verticies
            if(self.has_adjacent_color(vertex, coloring)):
                self.reset_used_colors()
                self.adjacent_colors(vertex, coloring)
                colors_intersection = self.available_colors()

                # select a random color that is not an adjacent color
                if(len(colors_intersection) > 0):
                    color_index = randint(0, len(colors_intersection))
                    if(color_index > 0):
                        color_index -= 1
                    coloring[vertex] = colors_intersection[color_index]
                else:
                    coloring[vertex] = 0
        return coloring



    def mutation2(self, chromosome):
        if(random() > self.mutation_rate):
            return chromosome

        coloring = chromosome

        # for each vertex in the chromosome
        for vertex in range(0, self.chromosome_length):
            # if vertex color has the same color as
            # adjacent colors
            if(self.has_adjacent_color(vertex, coloring)):
                # pick a random color and update
                color = randint(0, self.gene_length-1)
                coloring[vertex] = color

        return coloring


    def crossover(self, parent1, parent2, chromosome):
        if(random() > self.crossover_rate):
            return parent1.coloring

        crosspoint = randint(0, self.chromosome_length-1)

        for v in range(0, self.chromosome_length):
            if(v <= crosspoint):
                chromosome[v] = parent1.coloring[v]
            else:
                chromosome[v] = parent2.coloring[v]
        #child = Genome.from_chromosome(self.chromosome_length, self.gene_length, chromosome)
        return chromosome

    def form_consensus(self, vertex, population):
        counts = {}
        for i in range(0, len(population)):
            color = population[i].coloring[vertex]
            if(color in counts):
                counts[color] += 1
            else:
                counts[color] = 0


        highest_key = 0
        highest_val = 0
        for k, v in counts.items():
            if(v >= highest_val):
                highest_val = v
                highest_key = k
        return highest_key

    # Checks for bad edge in a vertex and uses the best half
    # of the population to form a concensus on what color works
    def wisdom_of_artificial_crowds(self):
        # get the best half of the of the final population
        experts = list()
        self.genomes.sort(key=lambda x: x.fitness, reverse=False)

        mid = int(self.population_size / 2)
        for i in range(0, mid):
            experts.append(self.genomes[i])

        aggregate = self.genomes[self.fittest_genome]

        coloring = aggregate.coloring
        for v in range(0, self.chromosome_length):
            if(self.has_adjacent_color(v, coloring)):
                # vertex is part of a bad edge, get consensus, and assign
                color = self.form_consensus(v, experts)
                coloring[v] = color

        chromosome = coloring

        coloring_map = {}
        for vertex in range(0, len(chromosome)):
            coloring_map[vertex] = chromosome[vertex]

        chromosome = self.genomes[self.fittest_genome].coloring
        color_set = set()

        for vertex in range(0, len(chromosome)):
            color_set.add(chromosome[vertex])
        return len(color_set), coloring_map
