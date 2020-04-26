from random import seed
from random import randint
from random import random

class Genome(object):
    def __init__(self, n_vertices, n_colors):
        seed()
        self.fitness = 0
        self.chromosome = list()

        for i in range(0, n_vertices):
            self.coloring.append(randint(0, n_colors))

class GeneAlg(object):
    def __init__(cross, mut, pop, bits, gene):
        self.crossover_rate = cross
        self.mutation_rate = mut
        self.population_size = pop
        self.chromosome_length = bits
        self.gene_length = gene
        self.generation = 0
        self.busy = False
        self.fittest_genome = 0
        self.best_fitness_score = 0
        self.genomes = list()

        self.create_start_population()

    def generation(self):
        return self.generation

    def fittest(self):
        return self.fittestGenome

    def chromosome(self):
        genome = self.genomes[fittestGenome]
        result = ""
        for i in range(genome.chromosome):
            result = result + genome.chromosome[i] + " "
        return result

    def started(self):
        return self.busy

    def stop(self):
        self.busy = False

    def update_fitness_score(self):
        self.fittest_genome = 0
        self.best_fitness_score = 0

        for i in range(0, self.population_size):
            chromosome = self.genomes[i].coloring
            #genomes[i].fitness = calcFitness###########################

            if(self.genomes[i].fitness < self.best_fitness_score):
                self.best_fitness_score = self.genomes[i].fitness
                self.fittest_genome = i

            if(self.genomes[i].fitness == 0):
                self.busy = false

            
    def create_start_population(self):
        self.genomes.clear()      
        for i in range(0, population_size):
            self.genomes.append(Genome(self.chromosome_length, self.gene_length))
        
        self.generation = 0
        self.fittest_genome = 0
        self.best_fitness_score = 0

    def run(self):
        self.create_start_population()
        self.busy = True

    def epoch(self):
        next_gen = list()
        self.update_fitness_score()
        noobs = 0

        while(noobs < self.population_size):
            #get parents
            #crossover
            #mutate
            noobs += 1
        self.genomes = next_gen
        self.generation += 1


