import csv
import fileinput
import pandas as pd

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

# TO_DO: draw complete graph for each set. Or list all combinations of 2 in each set as edges.

