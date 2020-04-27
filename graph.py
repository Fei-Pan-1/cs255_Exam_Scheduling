from random import seed
from random import random
from random import randint
from gene_alg import GeneAlg
import cProfile
import operator

# implementation of an undirected graph using Adjacency Lists
class EdgeNode(object):
    def __init__(self, source, target):
       self.source = source
       self.target = target

    def to_string(self):
        return " " + str(self.target)

class VertexNode(object):
    def __init__(self, v):
        self.vertex = v
        self.edges = list()
    
    # for sorting in Welsh Powell, we only care about length in lists
    def __eq__(self, other):
        return len(self.edges) == len(other.edges) and len(self.edges) == len(other.edges)

    def __lt__(self, other):
        return len(self.edges) < len(other.edges)

    def add_edge(self, u):
        self.edges.append(u)

    def contains(self, target):
        for edge in self.edges:
            if(edge.target == target):
                return True
        return False

    def to_string(self): 
        result = str(self.vertex) + ": "
        for edge in self.edges:
            result = result + str(edge.target) + " "
        return result

    def neighbors(self):
        return self.edges


class Graph(object):
    def __init__(self, n):
        self.adj_list = list()
        self.n_verticies = n
        self.n_edges = 0

        for i in range(0, n):
            self.adj_list.append(VertexNode(i))

    def vertices(self):
        return self.adj_list

    def add_edge(self, source, target):
        self.adj_list[source].add_edge(EdgeNode(source, target))
        self.adj_list[target].add_edge(EdgeNode(target, source))
        self.n_edges += 1

    def vertex(self, v):
        return self.adj_list[v]

    def neighbors_of(self, v):
        return self.adj_list[v].neighbors()

    def to_string(self):
        result = ""
        for vertex in self.adj_list:
            result = result + vertex.to_string() + "\n"
        return result

    @staticmethod
    def random_graph(n, probability_threshold):
        graph = Graph(n)

        for v1 in range(0, n):
            for v2 in range(0, n):
                if(v1 != v2 and random() < probability_threshold):
                    if(operator.not_(graph.vertex(v1).contains(v2)) and operator.not_(graph.vertex(v2).contains(v1))):
                        graph.add_edge(v1, v2)
        return graph
    
    @staticmethod
    def greedy_coloring(graph):
        coloring = {}
        color = 0

        for v in graph.vertices():
            # the case where the graph is disconnected and v
            # has no neighbors
            if len(v.neighbors()) <= 0:
                coloring[v.vertex] = color

            for neighbor in v.neighbors():
                if neighbor.target in coloring and coloring[neighbor.target] == color:
                    # this is an adjacent node with same color
                    # use next color
                    color += 1
                    coloring[v.vertex] = color
                else:
                    coloring[v.vertex] = color
        return coloring

    @staticmethod
    def graph_info(g):
        print("|V| = " + str(g.n_verticies) + " |E| = " + str(g.n_edges))



    @staticmethod
    def genetic_algorithm(graph):
        Graph.graph_info(graph)
        #parameters from paper
        mutation_rate = 0.7
        crossover_rate = 1.0
        population_size = 50
        # the paper has this set to 20,000 but without further
        # optimization, it takes too long to execute
        max_epochs = 20000

        #worst case, every vertex needs a color
        colors = len(graph.vertices())

        genetic = GeneAlg(crossover_rate, mutation_rate, population_size, graph.n_verticies, colors, graph)
        genetic.run()
        counter = 0
        while(genetic.started() and genetic.generations() < max_epochs):
            genetic.epoch()
            counter += 1
            if(counter == 100):
                print("Generation: " + str(genetic.generations()))
                counter = 0

        if(genetic.generations() >= max_epochs):
            print("Failed to Converge. Seeking wisdom of the crowds")
            coloring = genetic.wisdom_of_artificial_crowds()
            return genetic.n_colors_used(), coloring
        else:
            return genetic.n_colors_used(), genetic.coloring()

    @staticmethod
    def welsh_powell(graph):
        coloring_dict = {}
        vertices = graph.vertices()
        # sort vertices according to the decreasing number of their neighbors
        sorted_vertices = sorted(vertices, key=lambda kv: len(kv.neighbors()), reverse=True)
        #print('sorted_vertices:', [e.vertex for e in sorted_vertices])

        # Go through vertexes in the order of decreasing number of neighbors.
        color = 0
        for i in range(len(sorted_vertices)):
            v = sorted_vertices[i]
            # Skip if the vertex is already colored.
            if v.vertex in coloring_dict:
                continue
            # print('checking: ', v.vertex, [e.target for e in v.neighbors()])
            if i != 0:
                color += 1
            # Color the current vertex.
            coloring_dict[v.vertex] = color
            # A list of vertices that colored with the current color.
            colored = [v]

            # Try to color the rest vertices if possible.
            for j in range(i + 1, len(sorted_vertices)):
                u = sorted_vertices[j]
                if u.vertex not in coloring_dict:
                    hasColoredNeighbor = False
                    # Check if vertex u has any neighbor that colored with the current color.
                    # If vertex u doesn't have any neighbor colored with the current color, we color vertex u.
                    neighbors = set([x.target for x in u.neighbors()])
                    for w in colored:
                        # If find one vertex in current color list (colored) is u's neighbor,
                        # means vertex u has neighbor colored with the current color, we skip coloring vertex u.
                        if w.vertex in neighbors:
                            hasColoredNeighbor = True
                            break
                    # If vertex u doesn't have any neighbor colored with the current color, we color vertex u, and add
                    # it into the list of vertexes colored with the current color.
                    if not hasColoredNeighbor:
                        coloring_dict[u.vertex] = color
                        # print('color', u.vertex, 'to', color)
                        colored.append(u)
        return coloring_dict
    
    @staticmethod
    def is_valid_solution(coloring, g):
        for v in range(0, len(coloring)):
            neighbors = g.neighbors_of(v)
            for n in range(0, len(neighbors)):
                if(coloring[v] == coloring[neighbors[n].target]):
                    return False
        return True
            


def random_tests():
    iterations = 10
    max_nodes = 200
    correct_solutions = {}

    GREEDY = "Greedy"
    WP = "welsh_powell"
    GENETIC = "Genetic"

    correct_solutions[GREEDY] = 0
    correct_solutions[WP] = 0
    correct_solutions[GENETIC] = 0

    for i in range(0, iterations):
        print("Graph " + str(i))
        nodes = randint(0, max_nodes) + 1
        p = random()
        g = Graph.random_graph(nodes, p)
        Graph.graph_info(g)

        greedy_coloring = Graph.greedy_coloring(g)
        if(Graph.is_valid_solution(greedy_coloring, g)):
            correct_solutions[GREEDY] += 1

        wp_coloring = Graph.welsh_powell(g)
        if(Graph.is_valid_solution(wp_coloring, g)):
            correct_solutions[WP] += 1

        genetic_coloring = Graph.genetic_algorithm(g)
        if(Graph.is_valid_solution(genetic_coloring, g)):
            correct_solutions[GENETIC] += 1

    print("Greedy: " + str(correct_solutions[GREEDY])+ "/" + str(iterations))
    print("Welsh_Powell: " + str(correct_solutions[WP])+ "/" + str(iterations))
    print("Genetic: " + str(correct_solutions[GENETIC])+ "/" + str(iterations))


def main():
    seed()
    #random_tests()

    #g = Graph.random_graph(20, .7)
    #print('Graph:\n', g.to_string())
    #coloring = Graph.greedy_coloring(g)
    #print('Greedy Solution: \n',coloring)
    #print(str(len(g.vertices)))
    #coloring1 = Graph.welsh_powell(g)
    #print('Welsh Powell Solution: \n', coloring1)
    #cProfile.run('Graph.genetic_algorithm(Graph.random_graph(65, .2))')
    print(Graph.genetic_algorithm(Graph.random_graph(10, .4)))


if __name__ == '__main__':
    main()
