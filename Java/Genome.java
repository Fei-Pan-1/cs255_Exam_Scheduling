import java.util.List;
import java.util.ArrayList;
import java.util.Random;

public class Genome {
	List<Integer> chromosome;
	int fitness;

	public Genome(int nVerticies, int nColors) {
		Random random = new Random();
		chromosome = new ArrayList<>(nVerticies);
		fitness = 99999999;

		for(int i=0; i<nVerticies; i++) {
			chromosome.add(Integer.valueOf(random.nextInt(nColors)));
		}
	}

	public String toString() {
		String result = "Chromosome:  ";
		for(Integer i : chromosome) {
			result = result + i + " ";
		}
		result = result + ":::fitness: " + fitness;
		return result;
	}
}
