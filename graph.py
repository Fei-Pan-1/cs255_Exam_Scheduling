import csv
import fileinput

import pandas as pd

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
            # my YouTube video shows a silly for loop here, but this is a much faster way to do it
            self.vertices[u].add_neighbor(v)
            self.vertices[v].add_neighbor(u)
            return True
        else:
            return False

    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbors))

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
print(dmap)
print(df)


# TO_DO:draw complete graph for each set.


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