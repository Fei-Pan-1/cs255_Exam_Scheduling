from itertools import combinations
import pandas as pd
from graph import Graph

# Put each student and his exams in a dictionary.
# Student id is the key and a set of all exams of each student is the value.
df = pd.read_csv('dataset/processed_data/enrolments_with_id.csv')
df = df.drop(['student','exam'], axis=1)
# print(df)
dmap = {}
for row in df.values:
    dmap.setdefault(row[0], set()).add(row[1])
print(len(dmap), ' students: ', dmap)

df_exams = pd.read_csv('dataset/processed_data/exams.csv')
n = len(df_exams.index)
print(n, ' exams')

# List all combinations of 2 in each set as edges.
edges = set()
for key in dmap:
    exams_each_student = list(dmap[key])
    # print(exams_each_student)
    if len(exams_each_student) >= 2:
        lst = list(combinations(exams_each_student, 2))
        for l in lst:
            edges.add(l)

edges = sorted(edges, key=lambda edge: (edge[0], edge[1]))
print(len(edges), "edges(conflicts): ", edges)
df_edges = pd.DataFrame(edges, columns=['exam1', 'exam2'])
df_edges = df_edges.sort_values('exam1').reset_index(drop=True)
print(df_edges)
# df_edges.to_csv('dataset/processed_data/edges.csv', index=False)

graph = Graph(n)
for e in edges:
    u, v = e
    graph.add_edge(u, v)

print(graph.to_string())
coloring = Graph.greedy_coloring(graph)
print('Greedy Solution for Exams: \n',coloring, '\n', max(coloring.values()) + 1, ' colors used.')
# print(str(len(g.vertices)))
coloring1 = Graph.welsh_powell(graph)
print('Welsh Powell Solution for Exams: \n', coloring1, '\n', max(coloring1.values()) + 1, ' colors used.')

print('Beginning Genetic Algorithm: \n')
used, genetic_coloring = Graph.genetic_algorithm(graph, 38)
print('Genetic Algorithm Solution for Exams: \n',genetic_coloring, '\n', used, ' colors used.')

# Save welsh powell solution from dictionary to Dataframe
df_solution = pd.DataFrame(coloring1.items(), columns=['eid', 'tid'])
df_solution = df_solution.sort_values('eid').reset_index(drop=True)
print('Solution from Welsh-Powell:\n', df_solution)
# df_solution.to_csv('dataset/results/solution.csv', index=False)


wrong_color = 0
wrong_color1 = 0
wrong_color2 = 0
for e in edges:
    u, v = e
    # print(coloring1[u], coloring1[v])
    if coloring[u] == coloring[v]:
        wrong_color += 1
    if coloring1[u] == coloring1[v]:
        wrong_color1 += 1
    if genetic_coloring[u] == genetic_coloring[v]:
        wrong_color2 += 1
print(wrong_color, 'wrong color found in Greedy solution.')
print(wrong_color1, 'wrong color found in Welsh Powell solution.')
print(wrong_color1, 'wrong color found in Genetic solution.')
