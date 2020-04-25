import java.util.List;
import java.util.ArrayList;


public class GeneAlg {
	int MAX_EPOCHS, populationSize, geneLength, chromosomeLength;
	float crossoverRate, mutationRate;
	int fittestGenome, secondFittestGenome;
	float fittestScore;
	int generation;
	List<Genome> genomes;


	public GeneAlg(Graph graph, 
					int popSize,
					float crossRate,
					float mutRate,
					int gene_length,
					int max_epochs) {

		populationSize = popSize;
		crossoverRate = crossRate;
		mutationRate = mutRate;
		this.gene_length = gene_length; //n of colors
		chromosomeLength = graph.verticies().size();

		fittestGenome = -1;
		secondFittestGenome = -1;
		fittestScore = 999999;
		generation = 0;
		MAX_EPOCHS = max_epochs;

		genomes = new ArrayList<>(populationSize);

		for(int i=0; i<populationSize; i++) {
			genome = new Genome(chromosomeLength, gene_length);
			sccore = computeScore(genome.chromosome);
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
			int nextFittest = 999999;
			if(i != fittestGenome) {
				if(genome.fitness < nextFittest) {
					nextFittest = genome.fitness;
					secondFittestGenome = i;
				}
			}
		}
	}

	Genome maxFitness(Genome g1, Genome g2) {
		if(g1.fitness < g2.fitness) {
			return true;
		}
		return false;
	}

	Genome randomGenome() {
		return genomes[(int)Math.random()*populationSize-1]
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
		Genome parents = new Genome[2];
		parents[0] = genomes.get(fittestGenome);
		parents[1] = genomes.get(secondFittestGenome);

		return parents;
	}

	Genome crossover(Genome p1, Genome p2) {
		if(Math.random() > crossoverRate && p1 != p1) {
			return p1;
		}

		int crossoverPoint = (int)Math.random()*chromosomeLength-1;
		child = Genome(chromosomeLength, gene_length);

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
			if(coloring.get(vertex) == coloring.get(neighbor.target))
				return true;
		}
		return false;
	}

	List<Integer> colorMatchings(int vertex, List<Integer> coloring) {
		List<Integer> matchings = new ArrayList<>();
		List<EdgeNode> neighbors = graph.neighborOf(vertex);

		for(EdgeNode neighbor : neighbors) {
			if(coloring.get(vertex) == coloring.get(neighbor.target)) {
				matchings.add(new Integer(neighbor.target));
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

		for(int color=0; color<gene_length; color++) {
			if(!adjacentColors.contains(new Integer(color)) {
				validColors.add(new Integer(color));
			}
		}

		return validColors;
	}

	Genome mutation1(Genome g) {
		if(Math.random() > mutationRate) {
			return g;
		}

		for(int v=0; v<chromosomeLength; v++) {
			if(isColorMatching(v, g.chromosome)) {
				validColors = availableColors(v, g.chromosome);
				g.chromosome.set(v, validColors.get());
			}
		}
		return g;
	}

	Genome mutation2(Genome g) {
		if(Math.random() > mutationRate) {
			return g;
		}
		for(int v=0; v<chromosomeLength; v++) {
			if(isColorMatching(vertex, g.chromosome)) {
				g.chromosome.set(v, new Integer((int)Math.random()*gene_length-1))
			}
		}
		return g;
	}

	int computeScore(List<Integer> chromosome) {
		int badEdges = 0;

		for(Integer v : chromosome) {
			badEdges += colorMatchings(v, chromosome).size();
		}
		return badEdges;
	}

	public void updateFitnessScores() {
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
				child1 = crossover(parents[0], parents[1]);
				child1 = mutation1(child1);
				nextgen.add(child1);

				child2 = crossover(parents[1], parents[0]);
				child2 = mutation1(child2);
				nextgen.add(child2);
			} else {
				Genome[] parents = parentSelection2();
				child1 = crossover(parents[0], parents[1]);
				child1 = mutation2(child1);
				nextgen.add(child1);

				child2 = crossover(parents[1], parents[0]);
				child2 = mutation2(child2);
				nextgen.add(child2);
			}
			noobs++;
		}
		genomes = nextgen;
		generation++;
	}

	public Genome run() {
		while(fittestScore > 0 && generation <= MAX_EPOCHS) {
			epoch();
		}

		if(generation >= MAX_EPOCHS) {
			System.out.println("Failed");
		}
		return genomes.get(fittestGenome);
	}
}
