from random import seed
from random import randint
from random import random
seed()

class Genome:
    def __init__(self, n_vertices, n_colors):
        #length should be number of verticies
        #each is assigned a color from 0 to color-1
        self.chromosome = list()
        self.fitness = 999999999999

        for v in range(0, n_vertices):
            self.chromosome.append(randint(0, n_colors-1))

        #result = ""
        #for v in range(0, len(self.chromosome)):
            #result += str(self.chromosome[v])
        #print(result)

    def to_string(self):
        result = "Chromosome: "

        for i in range(0, len(self.chromosome)):
            result = result + str(self.chromosome[i]) + " "
        result = result + " :: fitness: " + str(self.fitness)

        return result

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
            self.fittest_score = 999999999999
            self.second_fittest_genome = 0
            self.generation = 0
            self.MAX_EPOCHS = max_epochs

    def create_initial_population(self):
        self.genomes.clear()

        for i in range(0, self.population_size):
            genome = Genome(self.chromosome_length, self.gene_length)
            chromosome = genome.chromosome
            score = 0

            for vertex in range(0, len(chromosome)):
                score += self.compute_score(vertex, chromosome)

            genome.fitness = score
            self.genomes.append(genome)

        self.generation = 0
        self.fittest_genome = 0
        self.second_fittest_genome = 0
        self.fittest_score = 999999999999


    def max_fitness(self, genome1, genome2):
        if(genome1.fitness < genome2.fitness):
            return genome1
        return genome2

    def random_genome(self):
        return self.genomes[randint(0, self.population_size-1)]

    def parent_selection1(self):
        tmp_parent1 = self.random_genome()
        tmp_parent2 = self.random_genome()
        parent1 = self.max_fitness(tmp_parent1, tmp_parent2)

        tmp_parent1 = self.random_genome()
        tmp_parent2 = self.random_genome()
        parent2 = self.max_fitness(tmp_parent1, tmp_parent2)

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

        crossover_point = randint(0, self.chromosome_length-1)
        child = Genome(self.chromosome_length, self.gene_length)

        for i in range(0, self.chromosome_length):
            if(i <= crossover_point):
                child.chromosome[i] = parent1.chromosome[i]
            else:
                child.chromosome[i] = parent2.chromosome[i]

        return child


#   Checks if a vertex has a matching color with any of 
#   its neighbors.

    def is_color_matching(self, vertex, coloring):
        neighbors = self.graph.neighbors_of(vertex)
        for neighbor in neighbors:
            if(coloring[vertex] == coloring[neighbor.target]):
                return True
        return False

#   creates a list of vertices whos colors match with 
#   a given vertex

    def color_matchings(self, vertex, coloring):
        matchings = list()
        neighbors = self.graph.neighbors_of(vertex)

        for neighbor in neighbors:
            if(coloring[vertex] == coloring[neighbor.target]):
                matchings.append(neighbor.target)
        return matchings

# creates a list of colors not used by neighbors 
# of a given vertex
    def available_colors(self, vertex, coloring):
        valid_colors = list()
        adjacent_colors = list()
        neighbors = self.graph.neighbors_of(vertex)

        for neighbor in neighbors:
            adjacent_colors.append(coloring[neighbor.target])
        

        for color in range(0, self.gene_length):
            if(color not in adjacent_colors):
                valid_colors.append(color)
        return valid_colors


    def mutation1(self, genome):
        if(random() < self.mutation_rate):
            chromosome = genome.chromosome
            for vertex in range(0, len(chromosome)):
                if(self.is_color_matching(vertex, chromosome)):
                    # we have neighbors with the same color
                    # get a list of available colors
                    valid_colors = self.available_colors(vertex, chromosome)
                    # assign vertex to valid random color
                    genome.chromosome[vertex] = valid_colors[randint(0, len(valid_colors)-1)]
        return genome


    def mutation2(self, genome):
        if(random() < self.mutation_rate):
            chromosome = genome.chromosome
            for vertex in range(len(chromosome)):
                if(self.is_color_matching(vertex, chromosome)):
                    genome.chromosome[vertex] = randint(0, self.gene_length-1)
        return genome

    def compute_score(self, vertex, chromosome):
        bad_edges = 0
        matching_verticies = self.color_matchings(vertex, chromosome)
        return len(matching_verticies)

# The fitness score is defined as the number of bad edges, where
# a bad edge is an edge between adjacent vertices with the same color.

    def update_fitness_scores(self):
        for i in range(0, len(self.genomes)):
            bad_edges = 0
            chromosome = self.genomes[i].chromosome

            for vertex in range(0, len(chromosome)):
                bad_edges = self.compute_score(vertex, chromosome)
            self.genomes[i].fitness = bad_edges
            
            if(self.genomes[i].fitness < self.fittest_score):
                self.second_fittest_genome = self.fittest_genome
                self.fittest_genome = i
                self.fittest_score = self.genomes[i].fitness

        # print("Generation: " + str(self.generation) + " fittest: " +str(self.fittest_score), end="\r", flush=True)

       # for i in range(0, len(self.genomes)):
       #     result = ""
       #     result = result + str(self.genomes[i].fitness) + ":::"
       #     chrome = self.genomes[i].chromosome
       ##     for j in range(0, len(chrome)):
        #        result = result + str(j)
        #    print(result)
        
    def epoch(self):
        # constant decided by paper through expermimentation
        SELECTION_MUTATION_THRESHOLD = 4
        next_generation = list()

        self.update_fitness_scores()

        noobs = 0
        while(noobs < self.population_size):
            if(self.fittest_score > 4):
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

 #       for g in self.genomes:
 #           result = ""
 #           chrome = g.chromosome
 ##           result = result + "F: " + str(g.fitness) + "::"
  #          for i in range(0, len(chrome)):
   #             result += str(chrome[i])
   #         print(result)

#TODO: Wisdom of the crowds

    def run(self):
        while(self.fittest_score > 0 and self.generation <= self.MAX_EPOCHS):
            self.epoch()

        if(self.generation == self.MAX_EPOCHS and self.fittest_score != 0):
            print("Failed to converge in "+ self.MAX_EPOCHS + " epochs")
            #wisdom of the crouds

        return self.genomes[self.fittest_genome]

