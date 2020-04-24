
# put each student's exams in a set.
import pandas as pd

df = pd.read_csv('dataset/processed_data/enrolments_with_id.csv')
df = df.drop(['student','exam'], axis=1)
print(df)
dmap = {}
for row in df.values:
    dmap.setdefault(row[0], set()).add(row[1])
print(dmap)

# TO_DO: list all combinations of 2 in each set as edges.

