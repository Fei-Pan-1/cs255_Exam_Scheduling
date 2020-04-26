from random import seed
from random import random
from gene_alg import GeneAlg
import operator

# implementation of an undirected graph using Adjacency Lists

class EdgeNode(object):
    def __init__(self, source, target):
       self.source = source
       self.target = target

    def to_string(self):
        return " " + str(target)

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

        for i in range(0, n):
            self.adj_list.append(VertexNode(i))

    def vertices(self):
        return self.adj_list

    def add_edge(self, source, target):
        self.adj_list[source].add_edge(EdgeNode(source, target))
        self.adj_list[target].add_edge(EdgeNode(target, source))

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
    def genetic_algorithm(graph):
        #parameters from paper
        mutation_rate = 1.0
        crossover_rate = 1.0
        population_size = 50
        max_epochs = 20000

        #worst case, every vertex needs a color
        colors = len(graph.vertices()) 
        #colors = 2

        genenetic = GeneAlg(graph, population_size, crossover_rate, mutation_rate, colors, max_epochs)
        coloring = genenetic.run()
        genomes = genenetic.genomes

        #for g in range(0, len(genomes)):
            #print(genomes[g].to_string())
        print("FITTESTSCORE:::"+str(genenetic.fittest_score))
        return coloring


    @staticmethod
    def welsh_powell(graph):
        coloring_dict = {}
        vertices = graph.vertices()
        # sort vertices according to the decreasing number of their neighbors
        sorted_vertices = sorted(vertices, key=lambda kv: len(kv.neighbors()), reverse=True)
        print('sorted_vertices:', [e.vertex for e in sorted_vertices])

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


def main():
    g = Graph.random_graph(5, .2)
    print('Graph:\n', g.to_string())
    coloring = Graph.greedy_coloring(g)
    print('Greedy Solution: \n',coloring)
    #print(str(len(g.vertices)))
    coloring1 = Graph.welsh_powell(g)
    print('Welsh Powell Solution: \n', coloring1)

if __name__ == '__main__':
    main()


g = Graph.random_graph(800, .7)
# print(g.to_string())
# g.print_graph()
coloring = Graph.greedy_coloring(g)
print('Greedy Solution: \n',coloring, '\n', max(coloring.values()) + 1, ' colors used.')
# print(str(len(g.vertices)))
coloring1 = Graph.welsh_powell(g)
print('Welsh Powell Solution: \n', coloring1, '\n', max(coloring1.values()) + 1, ' colors used.')
#print(g.vertices)
#colroing = Graph.genetic_algorithm(g)
#print("final:::" + colroing.to_string())



#class Vertex:
#    def __init__(self, n):
#        self.name = n
#        self.neighbors = list()
#
#    def add_neighbor(self, v):
#        if v not in self.neighbors:
#            self.neighbors.append(v)
#            self.neighbors.sort()
#
#class Graph:
#    vertices = {}
#
#    def add_vertex(self, vertex):
#        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
#            self.vertices[vertex.name] = vertex
#            return True
#        else:
#            return False
#
#    def add_edge(self, u, v):
#        if u in self.vertices and v in self.vertices:
#            self.vertices[u].add_neighbor(v)
#            self.vertices[v].add_neighbor(u)
#            return True
#        else:
#            return False
#
#    def print_graph(self):
#        for key in sorted(list(self.vertices.keys())):
#            print(key + str(self.vertices[key].neighbors))
#
#
#    @staticmethod
#    def greedy_coloring(graph):
#        coloring = {}
#        color = 0
#        vertices = graph.vertices
#
#        for v in vertices:
#            # the case where the graph is disconnected and v
#            # has no neighbors
#            if len(vertices[v].neighbors) <= 0:
#                coloring[v] = color
#
#            for neighbor in vertices[v].neighbors:
#                if neighbor in coloring and coloring[neighbor] == color:
#                    # this is an adjacent node with same color
#                    # use next color
#                    color += 1
#                    coloring[v] = color
#                else:
#                    coloring[v] = color
#        return coloring
#
#    # implementation of welsh_powell algorithm
#    def welsh_powell(graph):
#        coloring_dict = {}
#        vertices = graph.vertices
#
#        # sort vertices according to the decreasing number of their neighbors
#        sorted_vertices = sorted(vertices.items(), key=lambda kv: len(kv[1].neighbors), reverse = True)
#        #print(sorted_vertices)
#
#        color = -1
#        for v in sorted_vertices:
#            if v[0] in coloring_dict:
#                continue
#            # assign a new color
#            color += 1
#            coloring_dict[v[0]] = color
#            colored = [v]
#            for u in sorted_vertices:
#                if u[0] not in coloring_dict:
#                    #print('checking', u)
#                    isNeighborOfColored = False
#                    for w in colored:
#                        if u[0] in w[1].neighbors:
#                            #print(u[0], w[0])
#                            isNeighborOfColored = True
#                            break
#                    if not isNeighborOfColored:
#                        coloring_dict[u[0]] = color
#                        #print('color', u[0], 'to', color)
#                        colored.append(u)
#        return coloring_dict
#
#    @staticmethod
#    def random_graph(n, p_threshold):
#        seed()
#        g = Graph()
#        for vertex in range(0, n):
#            g.add_vertex(Vertex(str(vertex)))
#
#        for source in range(0, n):
#            for target in range(0, n):
#                #no self loops
#                if source != target and random() < p_threshold:
#                   if source not in g.vertices and source not in g.vertices:
#                        g.add_edge(str(source), str(target))
#        return g
#
#
#def main():
#    g = Graph.random_graph(5, .2)
#    g.print_graph()
#    coloring = Graph.greedy_coloring(g)
#    print('Greedy Solution: \n',coloring)
#    #print(str(len(g.vertices)))
#    coloring1 = Graph.welsh_powell(g)
#    print('Welsh Powell Solution: \n', coloring1)
#
#if __name__ == '__main__':
#    main()
