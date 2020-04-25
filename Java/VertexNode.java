private class VertexNode {
		public int vertex;
		public List<EdgeNode> edges;

		public VertexNode(int v) {
			vertex = v;
			edges = new ArrayList<EdgeNode>();
		}

		public List<EdgeNode> neighbors() { return edges; }

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