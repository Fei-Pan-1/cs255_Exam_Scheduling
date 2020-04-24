import pandas as pd

# Run one time only. So I comment out the statements.
# process students.csv and add 'sid' as a new column
df1 = pd.read_csv('dataset/processed_data/students.csv')
# df1.reset_index(inplace=True)
# df1.rename(columns = {'index':'sid'}, inplace = True)
# print(df1)
# df1.to_csv('dataset/processed_data/students.csv', index=False)

# process exams.csv and add 'eid' as a new column
df2 = pd.read_csv('dataset/processed_data/exams.csv')
# df2.reset_index(inplace=True)
# df2.rename(columns = {'index':'eid'}, inplace = True)
# print(df2)
# df2.to_csv('dataset/processed_data/exams.csv')

# process enrolments.csv
df3 = pd.read_csv('dataset/processed_data/enrolments.csv')
print(df3)
df3.to_csv('dataset/processed_data/enrolments.csv')
# df3 = df3.merge(df1).merge(df2)
# df3 = df3.drop(['major','description', 'duration', 'department_code'], axis=1)
# df3 = df3.sort_values('sid')
# df3 = df3.reset_index(drop=True)
# df3 = df3[["sid", "eid", "student", "exam"]]
# print(df3)
#df3.to_csv('dataset/processed_data/enrolments_with_id.csv')
