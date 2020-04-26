from random import seed
from random import randint
from random import random

INFINITY = float("inf")

class Genome(object):
    def __init__(self, n_vertices, n_colors):
        seed()
        self.fitness = INFINITY
        self.coloring = list()

        for i in range(0, n_vertices):
            self.coloring.append(randint(0, n_colors))

    @staticmethod
    def from_chromosome(n_vertices, n_colors, chromosome):
        g = Genome(n_vertices, n_colors)
        g.coloring = chromosome
        return g

class GeneAlg(object):
    def __init__(self, cross, mut, pop, bits, gene, graph):
        seed()
        self.crossover_rate = cross
        self.mutation_rate = mut
        self.population_size = pop
        self.chromosome_length = bits
        self.gene_length = gene
        self.generation = 0
        self.busy = False
        self.fittest_genome = 0
        self.best_fitness_score = INFINITY
        self.genomes = list()
        self.graph = graph

        self.create_start_population()

    def generations(self):
        return self.generation

    def fittest(self):
        return self.fittestGenome

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
        bad_edges = 0
        for vertex in range(0, len(chromosome)):
            adj_colors = self.adjacent_colors(vertex, chromosome)
            for color in range(0, len(adj_colors)):
                if(chromosome[vertex] == adj_colors[color]):
                    bad_edges += 1
        return bad_edges

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
        self.genomes.clear()      
        for i in range(0, self.population_size):
            self.genomes.append(Genome(self.chromosome_length, self.gene_length))
        
        self.generation = 0
        self.fittest_genome = 0
        self.best_fitness_score = INFINITY

    def run(self):
        self.create_start_population()
        self.busy = True

    def epoch(self):
        # constant defined in paper
        SELECTION_MUTTION_THRESHOLD = 4
        next_gen = list()
        self.update_fitness_score()
        noobs = 0

        # The paper discusses keeping the population size constant
        # but the psuedo-code does not mention how. So I think I 
        # can either create 2 children to replace the parents. Or
        # I can take the child and the fittest of the 2 parents
        # into the next generation. I will do the latter.

        while(noobs < self.population_size):
            if(self.best_fitness_score > SELECTION_MUTTION_THRESHOLD):
                parents = self.parent_selection1()
                child = self.crossover(parents[0], parents[1])
                child = self.mutation1(child)
                next_gen.append(child)

                parent = self.max_fitness(parents[0], parents[1])
                next_gen.append(parent)
            else:
                parents = self.parent_selection2()
                child = self.crossover(parents[0], parents[1])
                child = self.mutation2(child)
                next_gen.append(child)

                parent = self.max_fitness(parents[0], parents[1])
                next_gen.append(parent)

            noobs += 2
        self.genomes = next_gen
        self.generation += 1

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
        for v in range(0, len(neighbors)):
            if(coloring[vertex] == coloring[neighbors[v].target]):
                return True
        return False

    # Given a vertex, return a list of all colors
    # of adjacent verticies
    def adjacent_colors(self, vertex, coloring):
        colors = list()
        neighbors = self.graph.neighbors_of(vertex)

        for v in range(0, len(neighbors)):
            if(v != vertex):
                colors.append(coloring[neighbors[v].target])
        return colors

    def mutation1(self, genome):
        if(random() > self.mutation_rate):
            return genome

        coloring = genome.coloring
        new_coloring = list()

        # make a deep copy of the chromosome
        for i in range(0, len(coloring)):
            new_coloring.append(coloring[i])

        # for each vertex in the chromosome
        for vertex in range(0, len(coloring)):
            # if the vertex color has the same color as 
            # adjacent verticies
            if(self.has_adjacent_color(vertex, coloring)):
                adj_colors = self.adjacent_colors(vertex, coloring)
                # select a random color that is not an adjacent color
                color = randint(0, self.gene_length-1)
                while(color not in adj_colors):
                    color = randint(0, self.gene_length-1)

                # update color 
                new_coloring[vertex] = color
        g = Genome.from_chromosome(self.chromosome_length, self.gene_length, new_coloring)
        return g

    def mutation2(self, genome):
        if(random() > self.mutation_rate):
            return genome

        coloring = genome.coloring
        new_coloring = list()

        # make a deep copy of the chromosome
        for i in range(0, len(coloring)):
            new_coloring.append(coloring[i])

        # for each vertex in the chromosome
        for vertex in range(0, len(coloring)):
            # if vertex color has the same color as
            # adjacent colors
            if(self.has_adjacent_color(vertex, coloring)):
                # pick a random color and update
                color = randint(0, self.gene_length-1)
                new_coloring[vertex] = color

        g = Genome.from_chromosome(self.chromosome_length, self.gene_length, new_coloring)
        return g


    def crossover(self, parent1, parent2):
        if(random() > self.crossover_rate):
            return parent1

        crosspoint = randint(0, self.chromosome_length-1)
        chromosome = list()

        for v in range(0, self.chromosome_length):
            if(v <= crosspoint):
                chromosome.append(parent1.coloring[v])
            else:
                chromosome.append(parent2.coloring[v])
        child = Genome.from_chromosome(self.chromosome_length, self.gene_length, chromosome)
        return child

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
        return coloring
