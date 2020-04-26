import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Random;


public class GeneAlg {
	int MAX_EPOCHS, populationSize, geneLength, chromosomeLength;
	float crossoverRate, mutationRate;
	int fittestGenome, secondFittestGenome;
	float fittestScore;
	int generation;
	List<Genome> genomes;
	Graph graph;
	boolean busy;

	static Random random = new Random();


	public GeneAlg(Graph graph, 
					int popSize,
					float crossRate,
					float mutRate,
					int geneLength,
					int maxEpochs,
					int chromeLength) {

		populationSize = popSize;
		crossoverRate = crossRate;
		mutationRate = mutRate;
		this.geneLength = geneLength; //n of colors
		chromosomeLength = chromeLength;
		this.graph = graph;

		fittestGenome = -1;
		secondFittestGenome = -1;
		fittestScore = 999999;
		generation = 0;
		MAX_EPOCHS = maxEpochs;
		busy = false;
		

		genomes = new ArrayList<>(populationSize);

		for(int i=0; i<populationSize; i++) {
			Genome genome = new Genome(chromosomeLength, geneLength);
			int score = computeScore(genome.chromosome);
			genome.fitness = score;
			genomes.add(genome);

			//first fittest
			if(score <= fittestScore) {
				fittestScore = score;
				fittestGenome = i;
			}
		}

		int nextFittest = 999999;
		//second fittest separately just to be sure
		for(int i=0; i<populationSize; i++) {
			if(i != fittestGenome) {
				if(genomes.get(i).fitness < nextFittest) {
					nextFittest = genomes.get(i).fitness;
					secondFittestGenome = i;
				}
			}
		}
	}

	Genome maxFitness(Genome g1, Genome g2) {
		if(g1.fitness < g2.fitness) {
			return g1;
		}
		return g2;
	}

	Genome randomGenome() {
		return genomes.get(random.nextInt(populationSize));
	}

	Genome[] parentSelection1() {
		Genome[] parents = new Genome[2];
		Genome tmpParent1 = randomGenome();
		Genome tmpParent2 = randomGenome();
		parents[0] = maxFitness(tmpParent1, tmpParent2);

		tmpParent1 = randomGenome();
		tmpParent2 = randomGenome();
		parents[1] = maxFitness(tmpParent1, tmpParent2);

		return parents;
	}

	Genome[] parentSelection2() {
		Genome[] parents = new Genome[2];
		parents[0] = genomes.get(fittestGenome);
		parents[1] = genomes.get(secondFittestGenome);

		return parents;
	}

	Genome crossover(Genome p1, Genome p2) {
		if(random.nextFloat() > crossoverRate) {
			return p1;
		}

		int crossoverPoint = random.nextInt(chromosomeLength);
		Genome child = new Genome(chromosomeLength, geneLength);

		for(int i=0; i<chromosomeLength; i++) {
			if(i <= crossoverPoint) {
				child.chromosome.set(i, p1.chromosome.get(i));
			} else {
				child.chromosome.set(i, p2.chromosome.get(i));
			}
		}
		return child;
	}

	boolean isColorMatching(int vertex, List<Integer> coloring) {
		List<EdgeNode> neighbors = graph.neighborOf(vertex);

		for(EdgeNode neighbor : neighbors) {
			if(coloring.get(vertex) == coloring.get(neighbor.target) &&
				coloring.get(vertex) == coloring.get(neighbor.source))
				return true;
		}
		return false;
	}

	List<Integer> colorMatchings(int vertex, List<Integer> coloring) {
		List<Integer> matchings = new ArrayList<>();
		List<EdgeNode> neighbors = graph.neighborOf(vertex);

		for(EdgeNode neighbor : neighbors) {
			if(coloring.get(vertex) == coloring.get(neighbor.source) &&
				coloring.get(vertex) == coloring.get(neighbor.target)) {
				matchings.add(Integer.valueOf(neighbor.target));
			}
		}
		return matchings;
	}

	List<Integer> availableColors(int vertex, List<Integer> coloring) {
		List<Integer> validColors = new ArrayList<>();
		Set<Integer> adjacentColors = new HashSet<>();
		List<EdgeNode> neighbors = graph.neighborOf(vertex);

		for(EdgeNode neighbor : neighbors) {
			adjacentColors.add(coloring.get(neighbor.target));
		}

		for(int color=0; color<geneLength; color++) {
			if(!adjacentColors.contains(Integer.valueOf(color))) {
				validColors.add(Integer.valueOf(color));
			}
		}

		return validColors;
	}

	Genome mutation1(Genome g) {
		if(random.nextFloat() > mutationRate) {
			return g;
		}

		for(int v=0; v<chromosomeLength; v++) {
			if(isColorMatching(v, g.chromosome)) {
				List<Integer> validColors = availableColors(v, g.chromosome);
				g.chromosome.set(v, validColors.get(random.nextInt(validColors.size())));
			}
		}
		return g;
	}

	Genome mutation2(Genome g) {
		if(random.nextFloat() > mutationRate) {
			return g;
		}
		for(int v=0; v<chromosomeLength; v++) {
			if(isColorMatching(v, g.chromosome)) {
				g.chromosome.set(v, Integer.valueOf(random.nextInt(geneLength)));
			}
		}
		return g;
	}

	int computeScore(List<Integer> chromosome) {
		int badEdges = 0;

		for(int v=0; v<chromosome.size(); v++) {
			badEdges += colorMatchings(v, chromosome).size();
		}
		return badEdges;
	}

	public void updateFitnessScores() {
		fittestScore = 999999;
		fittestGenome = -1;
		secondFittestGenome = -1;

		for(int i=0; i<genomes.size(); i++) {
			Genome genome = genomes.get(i);
			int score = computeScore(genome.chromosome);
			genome.fitness = score;
			
			if(score <= fittestScore) {
				secondFittestGenome = fittestGenome;
				fittestGenome = i;
				fittestScore = score;
			}
			genomes.set(i, genome);

			if(genomes.get(i).fitness <= 0) {
				busy = false;
			}
		}

		int nextFittest = 999999;
		//second fittest separately just to be sure
		for(int i=0; i<populationSize; i++) {
			if(i != fittestGenome) {
				if(genomes.get(i).fitness < nextFittest) {
					nextFittest = genomes.get(i).fitness;
					secondFittestGenome = i;
				}
			}
		}
	}

	public void epoch() {
		int SELECTION_MUTATION_THRESHOLD = 4;
		List<Genome> nextgen = new ArrayList<>(populationSize);

		updateFitnessScores();

		int noobs = 0;
		while(noobs < populationSize) {
			if(fittestScore > 4) {
				Genome[] parents = parentSelection1();
				Genome child1 = crossover(parents[0], parents[1]);
				child1 = mutation1(child1);
				nextgen.add(child1);

				Genome child2 = crossover(parents[1], parents[0]);
				child2 = mutation1(child2);
				nextgen.add(child2);
			} else {
				Genome[] parents = parentSelection2();
				Genome child1 = crossover(parents[0], parents[1]);
				child1 = mutation2(child1);
				nextgen.add(child1);

				Genome child2 = crossover(parents[1], parents[0]);
				child2 = mutation2(child2);
				nextgen.add(child2);
			}
			noobs+=2;
		}
		genomes = nextgen;
		generation++;
		if(generation >= MAX_EPOCHS) {
			busy = false;
		}
	}

	public Genome run() {
		busy = true;
		while(busy) {
			epoch();
		}

		if(generation >= MAX_EPOCHS) {
			System.out.println("Failed");
		}

		Genome g = genomes.get(fittestGenome);
		System.out.println("Score: " + g.fitness);
		System.out.println("Generations: " + generation);
		return g;
	}
}
