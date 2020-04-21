import csv
import fileinput
import os
import stat

import pandas as pd
from random import seed
from random import random

# implementation of an undirected graph using Adjacency Lists
class Vertex:
    def __init__(self, n):
        self.name = n
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
                    #this is an adjacent node with same color
                    # use next color
                    color += 1
                    coloring[v] = color
                else:
                    coloring[v] = color
        return coloring

    # implementation of welsh_powell algorithm
    def welsh_powell(graph):
        coloring_dict = {}
        color = 0
        vertices = graph.vertices

        sorted_vertices = sorted(vertices.items(), key=lambda kv: len(kv[1].neighbors), reverse = True)
        #print('sorted', sorted_vertices)

        uncolored_vertices = sorted_vertices
        for v in uncolored_vertices:
            if v == sorted_vertices[0]:
                coloring_dict[v[0]] = 0
            else:
                color += 1
                coloring_dict[v[0]] = color
            uncolored_vertices.remove(v)
            #print('uncolored_vertices:', uncolored_vertices)

            for u in uncolored_vertices:
                if u not in v[1].neighbors:
                    coloring_dict[u[0]] = color
                    uncolored_vertices.remove(u)
        #print(coloring_dict)
        return coloring_dict

    @staticmethod
    def random_graph(n, p_threshold):
        seed()
        g = Graph()
        for vertex in range(0, n):
            g.add_vertex(Vertex(str(vertex)))

        for source in range(0, n):
            for target in range(0, n):
                #no self loops
                if source != target and random() < p_threshold:
                   if source not in g.vertices and source not in g.vertices:
                        g.add_edge(str(source), str(target))
        return g


def create_graph():
    g = Graph()

    return g



# covert txt file to csv file (add ',')
input_file = 'dataset/enrolments.txt'
output = open('dataset/enrolments_out.txt', 'w+')
'''
input_file = 'testdata/enrolments_test.txt'
output = open('testdata/enrolments_test_out.txt', 'w+')
'''
with output as f:
    for line in fileinput.input(input_file):
        line = line.split(None,2)
        f.write(','.join(line))
        f.write('\n')
read_file = pd.read_csv (r'dataset/enrolments_out.txt')
read_file.to_csv (r'dataset/enrolments.csv', index=None)

# put one student's exams in a set.
df = pd.read_csv('dataset/enrolments.csv')
df = df.sort_values(by=['Student'])
dmap = {}
for row in df.values:
    dmap.setdefault(row[0], set()).add(row[1])
#print(dmap)
#print(df)


g = Graph.random_graph(5, .2)
g.print_graph()
coloring = Graph.greedy_coloring(g)
print('Greedy Solution: \n',coloring)
#print(str(len(g.vertices)))
coloring1 = Graph.welsh_powell(g)
print('Welsh Powell Solution: \n', coloring1)

# TO_DO: draw complete graph for each set. Or list all combinations of 2 in each set as edges.


'''
g = Graph()
# print(str(len(g.vertices)))
a = Vertex('A')
g.add_vertex(a)
g.add_vertex(Vertex('B'))
for i in range(ord('A'), ord('K')):
    g.add_vertex(Vertex(chr(i)))

edges = ['AB', 'AE', 'BF', 'CG', 'DE', 'DH', 'EH', 'FG', 'FI', 'FJ', 'GJ', 'HI']
for edge in edges:
    g.add_edge(edge[:1], edge[1:])

g.print_graph()
'''
