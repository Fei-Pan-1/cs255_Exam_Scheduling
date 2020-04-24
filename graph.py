from random import seed
from random import random
from gene_alg import GeneAlg
import operator

# implementation of an undirected graph using Adjacency Lists

class EdgeNode:
    def __init__(self, source, target):
       self.source = source
       self.target = target

    def to_string(self):
        return " " + str(target)

class VertexNode:
    def __init__(self, v):
        self.vertex = v
        self.edges = list()

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


class Graph:
    def __init__(self, n):
        self.adj_list = list()
        self.n_verticies = n

        for i in range(0, n):
            self.adj_list.append(VertexNode(i))

    def vertices(self):
        return self.adj_list

    def add_edge(self, source, target):
        self.adj_list[source].add_edge(EdgeNode(source, target))
        self.adj_list[target].add_edge(EdgeNode(target, source))

    def vertex(self, v):
        return self.adj_list[v]

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
"""
    @staticmethod
    def genetic_algorithm(graph):
        #parameters from paper
        mutation_rate = 1.0
        crossover_rate = 1.0
        population_size = 50
        max_epochs = 20000

        #worst case, every vertex needs a color
        colors = len(graph.vertices) 

        genenetic = GeneAlg(graph, population_size, crossover_rate, mutation_rate, colors, max_epochs)
        genenetic.create_initial_population()
        coloring = genenetic.run()
        return coloring

    @staticmethod
    def greedy_coloring(graph):
        coloring = {}
        color = 0
        vertices = graph.vertices

        for v in vertices:
            # the case where the graph is disconnected and v
            # has no neighbors
            if len(vertices[v].neighbors) <= 0:
                coloring[v] = color

            for neighbor in vertices[v].neighbors:
                if neighbor in coloring and coloring[neighbor] == color:
                    # this is an adjacent node with same color
                    # use next color
                    color += 1
                    coloring[v] = color
                else:
                    coloring[v] = color
        return coloring

    # implementation of welsh_powell algorithm
    def welsh_powell(graph):
        coloring_dict = {}
        vertices = graph.vertices

        # sort vertices according to the decreasing number of their neighbors
        sorted_vertices = sorted(vertices.items(), key=lambda kv: len(kv[1].neighbors), reverse = True)
        #print(sorted_vertices)

        color = -1
        for v in sorted_vertices:
            if v[0] in coloring_dict:
                continue
            # assign a new color
            color += 1
            coloring_dict[v[0]] = color
            colored = [v]
            for u in sorted_vertices:
                if u[0] not in coloring_dict:
                    #print('checking', u)
                    isNeighborOfColored = False
                    for w in colored:
                        if u[0] in w[1].neighbors:
                            #print(u[0], w[0])
                            isNeighborOfColored = True
                            break
                    if not isNeighborOfColored:
                        coloring_dict[u[0]] = color
                        #print('color', u[0], 'to', color)
                        colored.append(u)
        return coloring_dict


    @staticmethod
    def random_graph(n, p_threshold):
        seed()
        g = Graph()
        for vertex in range(0, n):
            g.add_vertex(Vertex(str(vertex), vertex))

        for source in range(0, n):
            for target in range(0, n):
                #no self loops
                if source != target and random() < p_threshold:
                   if source not in g.vertices and source not in g.vertices:
                        g.add_edge(str(source), str(target))
        return g
"""

g = Graph.random_graph(5, .2)
print(g.to_string())
#g.print_graph()
#coloring = Graph.greedy_coloring(g)
#print('Greedy Solution: \n',coloring)
#print(str(len(g.vertices)))
#coloring1 = Graph.welsh_powell(g)
#print('Welsh Powell Solution: \n', coloring1)
#print(g.vertices)
#print(Graph.genetic_algorithm(g))

