from random import seed
from random import randint
from random import random
seed()

class Genome:
    def __init__(self, n_vertices, n_colors):
        #length should be number of verticies
        #each is assigned a color from 0 to color-1
        self.chromosome = list()
        self.fitness = 0.0

        for color in range(0, n_vertices):
            self.chromosome.append(randint(0, n_colors))

class GeneAlg:
    def __init__(self, graph, pop_size, cross_rate, mut_rate, gene_length, max_epochs):
            self.genomes = list()

            self.population_size = pop_size
            self.crossover_rate = cross_rate
            self.mutation_rate = mut_rate
            # number of vertices
            self.chromosome_length = len(graph.vertices())
            # number of colors
            self.gene_length = gene_length
            self.graph = graph

            self.fittest_genome = 0
            self.fittest_score = 0
            self.second_fittest_genome = 0
            self.generation = 0
            self.MAX_EPOCHS = max_epochs

    def create_initial_population(self):
        self.genomes.clear()

        for i in range(0, self.population_size):
            self.genomes.append(Genome(self.chromosome_length, self.gene_length))

        self.generation = 0
        self.fittest_genome = 0
        self.second_fittest_genome = 0
        self.fittest_score = 0


    def max(genome1, genome2):
        if(genome1.fitness > genome2):
            return genome1
        return genome2

    def random_genome(self):
        return self.genomes[randint(0, self.population_size-1)]

    def parent_selection1(self):
        tmp_parent1 = self.random_genome()
        tmp_parent2 = self.random_genome()
        parent1 = max(tmp_parent1, tmp_parent2)

        tmp_parent1 = self.random_genome()
        tmp_parent2 = self.random_genome()
        parent2 = max(tmp_parent1, tmp_parent2)

        return parent1, parent2

#   parent1 = the top performing chromosome;
#   parent2 = the top performing chromosome;

    def parent_selection2(self):
        parent1 = self.genomes[self.fittest_genome]
        parent2 = self.genomes[self.second_fittest_genome]

        return parent1, parent2

#       crosspoint = random point along a chromosome;
#       child = colors up to and including crosspoint from parent 1 +
#       colors after crosspoint to the end of the chromosome from
#       parent2;

    def crossover(self, parent1, parent2):
        if((random() > self.crossover_rate) and (parent1 != parent1)):
            #don't corossover
            return parent1, parent2

        crossover_point = randint(0, self.chromosome_length)
        child = Genome(self.chromosome_length, self.gene_length)

        #range is (inclusive, exclusive)
        for i in range(0, crossover_point+1):
            child.chromosome[i] = parent1.chromosome[i]

        for i in range(crossover_point+2, self.chromosome_length):
            child.chromosome[i] = parent2[i]

        return child


#   Checks if a vertex has a matching color with any of 
#   its neighbors.

    def is_color_matching(self, vertex, coloring):

        neighbors = graph.neighbors_of(vertex)
        for neighbor in neighbors:
            if(coloring[vertex] == coloring[neighbor.index]):
                return True
        return False

#   creates a list of vertices whos colors match with 
#   a given vertex

    def color_matchings(self, vertex, coloring):
        matchings = list()
        neighbors = self.graph.neighbors_of(vertex)

        for neighbor in neighbors:
            #print("asdfasdfasfasdfsadfa"+neighbor)
            if(coloring[vertex] == coloring[neighbor.index]):
                matchings.append(neighbor.index)
        return matchings

# creates a list of colors not used by neighbors 
# of a given vertex
    def available_colors(self, vertex, adjacent_colors):
        valid_colors = list()
        neighbors = graph.neighbors_of(vertex)
        

        for color in range(0, self.gene_length):
            if(color not in adjacent_colors):
                valid_colors.append(color)
        return valid_colors


    def mutation1(self, genome):
        if(random() < self.mutation_rate):
            chromosome = genome.chromosome
            for vertex in range(len(chromosome)):
                if(is_color_matching(vertex, chromosome)):
                    # we have neighbors with the same color
                    # get a list of available colors
                    valid_colors = available_colors(vertex, chromosome)
                    # assign vertex to valid random color
                    genome.chromosome[vertex] = valid_colors[randint(0, len(valid_colors))]
        return genome


    def mutation2(self, genome):
        if(random() < self.mutation_rate):
            chromosome = genome.chromosome
            for vertex in range(len(chromosome)):
                if(is_color_matching(vertex, chromosome)):
                    genome.chromosome[vertex] = randint(0, gene_length)
        return genome

# The fitness score is defined as the number of bad edges, where
# a bad edge is an edge between adjacent vertices with the same color.

    def update_fitness_scores(self):
        for i in range(0, len(self.genomes)):
            bad_edges = 0
            chromosome = self.genomes[i].chromosome

            for vertex in chromosome:
                matching_verticies = self.color_matchings(vertex, chromosome)
                bad_edges += len(matching_verticies)
            self.genomes[i].fitness = bad_edges
            
            if(genome[i].fitness > fittest_so_far):
                self.second_fittest_genome = self.fittest_genome
                self.fittest_genome = i
                self.fittest_score = genome[i].fitness

        
    def epoch(self):
        # constant decided by paper through expermimentation
        SELECTION_MUTATION_THRESHOLD = 4
        fittest_score = self.genomes[self.fittest_genome].fitness
        next_generation = list()

        self.update_fitness_scores()

        noobs = 0
        while(noobs < self.population_size):
            if(fittest_score > 4):
                parent1, parent2 = self.parent_selection1()
                child1 = self.crossover(parent1, parent2)
                child1 = self.mutation1(child1)
                next_generation.append(child1)

                child2 = self.crossover(parent1, parent2)
                child2 = self.mutation1(child2)
                next_generation.append(child2)

            else:
                parent1, parent2 = self.parent_selection2()
                child1 = self.crossover(parent1, parent2)
                child1 = self.mutation2(child1)
                next_generation.append(child1)

                child2 = self.crossover(parent1, parent2)
                child2 = self.mutation2(child2)
                next_generation.append(child2)
            noobs += 1

        self.genomes = next_generation
        self.generation += 1

#TODO: Wisdom of the crowds

    def run(self):
        while(self.fittest_score != 0 or self.generation <= self.MAX_EPOCHS):
            self.epoch()

        if(self.generation == MAX_EPOCHS and self.fittest_score != 0):
            print("Failed to converge in "+ self.MAX_EPOCHS + " epochs")
            #wisdom of the crouds

        return self.genomes[fittest_genome]

