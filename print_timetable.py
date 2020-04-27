import pandas as pd


# print out time table
df_exams = pd.read_csv('dataset/processed_data/exams.csv')
df_timeslots = pd.read_csv('dataset/processed_data/timeslots.csv')
df_solution = pd.read_csv('dataset/processed_data/solution.csv')

# assign room for each exam. Exams at same time slot should be in different rooms
# df_solution = df_solution.sort_values('tid').reset_index(drop=True)
# room_col = []
# room_col.append(0)
# for index, row in df_solution.iterrows():
#     room = 0
#     prev_row['tid']
#     if index = 0:
#     print(index, row['eid'], row['tid'])
# print(df_exams)

# print(df_solution)
df_timetable_draft = pd.merge(df_exams, df_solution, on='eid')
# print(df_timetable_draft)
df_timetable = pd.merge(df_timetable_draft, df_timeslots, on='tid')
df_timetable = df_timetable.sort_values('eid').reset_index(drop=True)
df_timetable = df_timetable.drop(columns=['duration','department_code'], axis=1)
print(df_timetable)
df_timetable.to_csv('dataset/processed_data/timetable.csv', index=False)