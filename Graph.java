import java.util.List;
import java.util.ArrayList;

public class Graph {
	private List<List<EdgeNode>> adjList;
	public int nVertices;
	private int nEdges;

	private class EdgeNode {
		public int source;
		public int target;

		public EdgeNode(int source, int target) {
			this.source = source;
			this.target = target;
		}

		public String toString() {
			return " " + target;
		}
	}

	public Graph(int n) {
		nVertices = n;
		adjList = new ArrayList<List<EdgeNode>>(n);

		for(int i=0; i<n; i++) {
			adjList.add(new ArrayList<EdgeNode>());
		}
	}

	public boolean vertexContains(int source, int target) {
		List<EdgeNode> edges = adjList.get(source);
		for(EdgeNode edge: edges) {
			if(edge.target == target) {
				return true;
			}
		}
		return false;
	}

	public void addEdge(int source, int target) {
		adjList.get(source).add(new EdgeNode(source, target));
	}

	public String toString() {
		int vertex = 0;
		String result = new String();

		for(List<EdgeNode> edges: adjList) {
			result =  result + vertex + ":";
			for(EdgeNode edge: edges) {
				result = result + edge.toString();
			}
			vertex++;
			result += "\n";
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
					if(!graph.vertexContains(v1, v1) &&
						!graph.vertexContains(v2, v1)) {
						graph.addEdge(v1, v2);
						graph.addEdge(v2, v1);

					}
				}
			}
		}
		return graph;
	}

	public static void main(String[] args) {
		Graph g = Graph.randomGraph(10, .4);
		System.out.println(g.toString());
	}
}
