import java.util.List;
import java.util.ArrayList;

public class Graph {
	private List<VertexNode> adjList;
	public int nVertices;

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

	private class VertexNode {
		public int vertex;
		public List<EdgeNode> edges;

		public VertexNode(int v) {
			vertex = v;
			edges = new ArrayList<EdgeNode>();
		}

		public void addEdge(EdgeNode e) {
			edges.add(e);
		}

		public boolean contains(int target) {
			for(EdgeNode edge : edges) {
				if(edge.target == target) {
					return true;
				}
			}
			return false;
		}

		public String toString() {
			String result = new String(vertex + ": ");
			for(EdgeNode edge : edges) {
				result = result + edge.target + " ";
			}
			return result;
		}
	}

	public Graph(int n) {
		nVertices = n;
		adjList = new ArrayList<VertexNode>(n);

		for(int i=0; i<n; i++) {
			adjList.add(new VertexNode(i));
		}
	}

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

	public static void WelshPowell(Graph g) {

	}

	public static void main(String[] args) {
		Graph g = Graph.randomGraph(10, .4);
		System.out.println(g.toString());
	}
}
