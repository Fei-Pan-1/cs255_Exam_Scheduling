from itertools import combinations
import pandas as pd
from graph import Graph
from graph import Vertex

# put each student and his exams in a dictionary.
df = pd.read_csv('dataset/processed_data/enrolments_with_id.csv')
df = df.drop(['student','exam'], axis=1)
print(df)
dmap = {}
for row in df.values:
    dmap.setdefault(row[0], set()).add(row[1])
print(dmap)

# list all combinations of 2 in each set as edges.
edges = []
for key in dmap:
    exams_each_student = list(dmap[key])
    # print(exams_each_student)
    if len(exams_each_student) >= 2:
        lst = list(combinations(exams_each_student, 2))
        for l in lst:
            edges.append(l)

print(len(edges), "edges: ", edges)
df_edges = pd.DataFrame(edges, columns=['exam1', 'exam2'])
df_edges = df_edges.sort_values('exam1')
print(df_edges)
#df_edges.to_csv('dataset/processed_data/edges.csv', index=False)

graph = Graph()
for e in edges:
    u_s, v_s = e
    u = Vertex(u_s)
    v = Vertex(v_s)
    # graph.add_vertex(u)
    # graph.add_vertex(v)
    # graph.add_edge(u, v)

graph.print_graph()