#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pulp import *

# Define problem and variables
prob = LpProblem("NurseSchedulingProblem", LpMinimize)# 問題を定義し、最小化を目指すことを設定
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']# 曜日のリスト
nurses = ['Nurse 1', 'Nurse 2', 'Nurse 3', 'Nurse 4', 'Nurse 5', 'Nurse 6', 'Nurse 7', 'Nurse 8', 'Nurse 9', 'Nurse 10']# ナースのリスト
shifts = ['Day', 'Night', 'Late Night'] # シフトのリスト
shift_requirements = {'Day': 3, 'Night': 2, 'Late Night': 1}# 各シフト毎の勤務人数
workday_requirements = {'Nurse 1': 5, 'Nurse 2': 5, 'Nurse 3': 5, 'Nurse 4': 5, 'Nurse 5': 5, 'Nurse 6': 5, 'Nurse 7': 5, 'Nurse 8': 5, 'Nurse 9': 5, 'Nurse 10': 5}# 各ナースの必要な勤務日数


# In[2]:


# Create decision variables
shifts_worked = LpVariable.dicts("ShiftsWorked", (nurses, days, shifts), cat='Binary')# 各ナースが各日の各シフトに割り当てられるかどうか

# Define objective function
prob += lpSum([shifts_worked[nurse][day][shift] for nurse in nurses for day in days for shift in shifts])# 目的関数を定義し、各ナースが働くシフトの総和を最小化

print(prob)# 変数と目的関数を表示


# In[4]:


# Define hard constraints
for day in days:
    for shift in shifts:
        prob += lpSum([shifts_worked[nurse][day][shift] for nurse in nurses]) == shift_requirements[shift], f"ShiftRequirement_{day}_{shift}" # 各日の各シフトの要件を満たす制約を設定
for nurse in nurses:
    prob += lpSum([shifts_worked[nurse][day][shift] for day in days for shift in shifts]) == workday_requirements[nurse], f"WorkdayRequirement_{nurse}" # 各ナースの必要な勤務日数を満たす制約を設定

print(prob)# 変数，目的関数，最低条件を表示
    
# Define soft constraints
for nurse in nurses:
    for i in range(len(days)-1):
        # 3日連続で日勤シフトに入らない制約を設定
        prob += shifts_worked[nurse][days[i]]['Day'] + shifts_worked[nurse][days[i+1]]['Day'] + shifts_worked[nurse][days[i+2]]['Day'] <= 2, f"No3StraightDays_{nurse}_{days[i]}"  
         # 制約：ナースは深夜勤務を2日連続で行わない（曜日は問わない）
        prob += shifts_worked[nurse][days[i]]['Late Night'] + shifts_worked[nurse][days[(i+1)%len(days)]]['Late Night'] <= 1, f"NoConsecutiveLateNights_{nurse}_{days[i]}"
　　　　for i in range(len(days)-2): # len(days)-1 を len(days)-2 に変更
        # 制約：ナースは3日連続で勤務しない（シフトは問わない）
        prob += lpSum([shifts_worked[nurse][days[i+j]][shift] for j in range(3) for shift in shifts]) <= 2, f"No3StraightDays_{nurse}_{days[i]}"  
           
print(prob)# 変数，目的関数，最低条件，オプション条件を表示


# In[9]:


# Solve problem and print solution
prob.solve() # 問題を解く
print("Status:", LpStatus[prob.status]) # 問題のステータスを出力
for nurse in nurses:
    print("Nurse:", nurse)
    for day in days:
        for shift in shifts:
            if shifts_worked[nurse][day][shift].value() == 1:
                print(f"\t{day}: {shift}") # 割り当てられたシフトを出力

