from random import seed
from random import random
from gene_alg import GeneAlg

# implementation of an undirected graph using Adjacency Lists
"""
class Vertex:
    def __init__(self, n, index):
        self.name = n
        self.index = index
        self.neighbors = list()

    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()


class Graph:
    vertices = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add_neighbor(v)
            self.vertices[v].add_neighbor(u)
            return True
        else:
            return False

    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbors))

#TODO: will need to adjust this to work with exams
    def neighbors_of(self, i_vertex):
        for v in self.vertices:
            print(v)
        return self.vertices[str(i_vertex)].neighbors
"""
class EdgeNode:
   def __init__(self, source, target):
       self.source = source
       self.target = target

    def to_string(self):
        return " " + target

class VertexNode:
    def __init__(self, v):
        self.vertex = v
        self.edges = list()

    def add_edge(self, u):
        edges.append(u)

    def contains(self, target):
        for edge in edges:
            if(edge.target == target):
                return True
        return False

    def to_string(self): 
        result = self.vertex + ": "
        for edge in self.edges:
            result = result + edge.target + " "

        return result


class Graph
    def __init__(self, n):
        self.adjList = list()
        for i in range(0, n):
            self.adjList.append(VertexNode(i))

    def vertices(self):
        return self.adjList

    def add_edge(source, target):
        self.adjList[source].add_edge(EdgeNode(source, target))

    def vertex(v)
        return self.adjList[v]

    def to_string():
        result = ""
        for vertex in adjList:
            result = result + vertex.to_string() + "\n"
        return result

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
"""
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
#g.print_graph()
#coloring = Graph.greedy_coloring(g)
#print('Greedy Solution: \n',coloring)
#print(str(len(g.vertices)))
#coloring1 = Graph.welsh_powell(g)
#print('Welsh Powell Solution: \n', coloring1)
#print(g.vertices)
print(Graph.genetic_algorithm(g))

