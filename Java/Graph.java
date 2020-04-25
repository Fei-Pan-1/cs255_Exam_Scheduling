import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;

public class Graph {
	private List<VertexNode> adjList;
	public int nVertices;

	public Graph(int n) {
		nVertices = n;
		adjList = new ArrayList<VertexNode>(n);

		for(int i=0; i<n; i++) {
			adjList.add(new VertexNode(i));
		}
	}

	public List<EdgeNode> neighborOf(int vertex) {
		return adjList.get(vertex).neighbors();
	}

	public List<VertexNode> verticies() { return adjList; }

	public void addEdge(int source, int target) {
		adjList.get(source).addEdge(new EdgeNode(source, target));
	}

	public VertexNode vertex(int v) {
		return adjList.get(v);
	}

	public String toString() {
		String result = new String();
		for(VertexNode vertex : adjList) {
			result = result + vertex.toString() + "\n";
		}

		return result;
	}

	//https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model
	public static Graph randomGraph(int n, double probabilityThreshold) {
		Graph graph = new Graph(n);

		for(int v1=0; v1<graph.nVertices; v1++) {
			for(int v2=0; v2<graph.nVertices; v2++) {
				if(v1 != v2 && //no self loops
					Math.random() < probabilityThreshold) {
					//since the graph is undirected, we shouldn't add edges
					//if there is already an edge
					if(!graph.vertex(v1).contains(v2) &&
						!graph.vertex(v2).contains(v1)) {
						graph.addEdge(v1, v2);
						graph.addEdge(v2, v1);

					}
				}
			}
		}
		return graph;
	}

	public static Genome geneticAlgorithm(Graph graph) {
		mutationRate = 1.0;
		crossoverRate = 1.0;
		populationSize = 50;
		maxEpochs = 20000;
		colors = graph.verticies().size();

		GenAlg genetic = new GeneAlg(graph,
									populationSize,
									crossoverRate,
									mutationRate,
									colors,
									maxEpochs);
		Genome chromosome = genetic.run();
		return chromosome;
	}


	public static Map<Integer, Integer> greedyColoring(Graph graph) {
		Map<Integer, Integer> coloring = new HashMap<>();
		for(VertexNode v : graph.verticies()) {
			coloring.put(v.vertex, -1);
		}


		int color = 0;
		for(VertexNode v : graph.verticies()) {
			if(v.edges.size() <= 0) {
				coloring.put(v.vertex, color);
			}
			for(EdgeNode neighbor: v.edges) {
				//if the neighbor has been colored
				if(coloring.containsKey(neighbor.target)) {
					if(coloring.get(neighbor.target) == color) {
						//we have an adjacent node with the same color
						color++;//use next color
						coloring.put(v.vertex, color);
					} else {
						//use the same color
						coloring.put(v.vertex, color);
					}
				}
			}
		}
		return coloring;
	}

	public static String coloringToString(Map<Integer, Integer> coloring) {
		String result = new String();
		for(Integer v : coloring.keySet()) {
			result = result + "Vertex: " + v + "  Coloring: " + coloring.get(v);
		}
		return result;
	}

	public static void main(String[] args) {
		Graph g = Graph.randomGraph(4, .2);
		//Map<Integer, Integer> coloring = Graph.greedyColoring(g);
		//System.out.println(coloring.toString());
		System.out.println(g.toString());
		//System.out.println(coloringToString(coloring));
		Genome gen = Graph.geneticAlgorithm(g);

	}
}
