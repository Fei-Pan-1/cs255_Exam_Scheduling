import pandas as pd


# print out time table
df_exams = pd.read_csv('dataset/processed_data/exams.csv')
df_timeslots = pd.read_csv('dataset/processed_data/timeslots.csv')
df_solution = pd.read_csv('dataset/results/solution.csv')

# assign rooms for each exam. Exams at same time slot should be in different rooms
df_solution = df_solution.sort_values('tid').reset_index(drop=True)
nextRoom = {}
assigned_room = []
for index, row in df_solution.iterrows():
    print(index, row['eid'], row['tid'])
    roomNo = nextRoom.get(row['tid'], 0)
    assigned_room.append(roomNo)
    nextRoom[row['tid']] = roomNo + 1
print(assigned_room)

# add room column to solution
df_solution['rid'] = assigned_room
print(df_solution)
# df_solution.to_csv('dataset/results/solution.csv', index=False)

df_timetable_draft = pd.merge(df_exams, df_solution, on='eid')
print(df_timetable_draft)
df_timetable = pd.merge(df_timetable_draft, df_timeslots, on='tid')
df_timetable = df_timetable.sort_values('eid').reset_index(drop=True)
df_timetable = df_timetable.drop(columns=['duration','tid'], axis=1)
# rename the columns
df_timetable.columns = ['Exam Id','Exam','Description','Department','Room','Start Time','End Time','Date']
# reorder the columns
df_timetable = df_timetable[['Exam Id','Exam','Description','Department','Start Time','End Time','Date','Room']]
df_timetable = df_timetable.sort_values('Department').reset_index(drop=True)
print(df_timetable)

df_timetable.to_csv('dataset/results/timetable.csv', index=False)