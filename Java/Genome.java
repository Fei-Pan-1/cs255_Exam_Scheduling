	class Genome(nVerticies, nColors) {
		List<Integer> chromosome;
		int fitness;

		public Genome(nVerticies, nColors) {
			chromosome = new ArrayList<>(nVerticies);

			for(int i=0; i<nVerticies; i++) {
				chromosome.add(new Integer(Math.random() * nColors);
			}
		}

		public String toString() {
			result = "Chromosome:  ";
			for(Integer i : chromosome) {
				result = result + i + " ";
			}
			result = result + ":::fitness: " + fitness;
		}
	}