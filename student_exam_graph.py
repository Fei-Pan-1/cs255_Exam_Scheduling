from itertools import combinations
import pandas as pd

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
    lst = list(combinations(exams_each_student, 2))
    edges.append(lst)

print(len(edges), "edges: ", edges)