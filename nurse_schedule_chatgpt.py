#!/usr/bin/env python
# coding: utf-8

# In[6]:


from pulp import *

# Define problem and variables
prob = LpProblem("NurseSchedulingProblem", LpMinimize)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
nurses = ['Nurse 1', 'Nurse 2', 'Nurse 3', 'Nurse 4', 'Nurse 5', 'Nurse 6', 'Nurse 7', 'Nurse 8', 'Nurse 9', 'Nurse 10']
shifts = ['Day', 'Night', 'Late Night']
shift_requirements = {'Day': 3, 'Night': 2, 'Late Night': 1}
workday_requirements = {'Nurse 1': 5, 'Nurse 2': 5, 'Nurse 3': 5, 'Nurse 4': 5, 'Nurse 5': 5, 'Nurse 6': 5, 'Nurse 7': 5, 'Nurse 8': 5, 'Nurse 9': 5, 'Nurse 10': 5}


# In[7]:


# Create decision variables
shifts_worked = LpVariable.dicts("ShiftsWorked", (nurses, days, shifts), cat='Binary')

# Define objective function
prob += lpSum([shifts_worked[nurse][day][shift] for nurse in nurses for day in days for shift in shifts])


# In[8]:


# Define hard constraints
for day in days:
    for shift in shifts:
        prob += lpSum([shifts_worked[nurse][day][shift] for nurse in nurses]) == shift_requirements[shift], f"ShiftRequirement_{day}_{shift}"
for nurse in nurses:
    prob += lpSum([shifts_worked[nurse][day][shift] for day in days for shift in shifts]) == workday_requirements[nurse], f"WorkdayRequirement_{nurse}"

# Define soft constraints
for nurse in nurses:
    for i in range(len(days)-1):
        if i < len(days)-2 and i+1 < len(days) and i+2 < len(days):
            prob += shifts_worked[nurse][days[i]]['Late Night'] + shifts_worked[nurse][days[i+1]]['Day'] <= 1, f"NoLateNightToDayShift_{nurse}_{days[i]}"
        prob += shifts_worked[nurse][days[i]]['Day'] + shifts_worked[nurse][days[i+1]]['Day'] + shifts_worked[nurse][days[i+2]]['Day'] <= 2, f"No3StraightDays_{nurse}_{days[i]}"
    prob += shifts_worked[nurse]['Saturday']['Late Night'] + shifts_worked[nurse]['Sunday']['Late Night'] <= 1, f"LateNightNot2Days_{nurse}"


# In[9]:


# Solve problem and print solution
prob.solve()
print("Status:", LpStatus[prob.status])
for nurse in nurses:
    print("Nurse:", nurse)
    for day in days:
        for shift in shifts:
            if shifts_worked[nurse][day][shift].value() == 1:
                print(f"\t{day}: {shift}")


# In[ ]:




