# File to read data from csv and compute graphs with boxplo
import pandas as pd
from pandas import read_csv, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import math

labels = ['Random', 'Beginner', 'Expert', 'Pro']
left = [1,2,3,4]

# Create Data Frames
# Read Data
rand = read_csv('results/random.csv')
rand_df = pd.DataFrame(rand)
beg = read_csv('results/beginner.csv')
beg_df = pd.DataFrame(beg)
exp = read_csv('results/expert.csv')
exp_df = pd.DataFrame(exp)
pro = read_csv('results/pro.csv')
pro_df = pd.DataFrame(pro)
dfs = [rand_df, beg_df, exp_df, pro_df]

# Win percentage 

s = [0,0,0,0]
total= [len(rand_df), len(beg_df), len(exp_df), len(pro_df)]
wp = [0,0,0,0]
soma = 0

i = 0
for df in dfs:
    for index, row in df.iterrows():
        if row[0] == 1:
            soma += 1
    wp[i] = soma / total[i]
    soma = 0
    i += 1

print(wp)

plt.bar(left, wp, tick_label=labels, width=0.8, color = ['red', 'orange', 'yellow', 'green'])
plt.xlabel('Players')
plt.ylabel('Win %')
plt.title('Win Percentage')
plt.savefig('win_perc.png')
plt.show()

# Point Average with confidence interval
pt = [0,0,0,0]
games_played = [len(rand_df), len(beg_df), len(exp_df), len(pro_df)]
avg_points = [0,0,0,0]
values = [[],[],[],[]]

i = 0
for df in dfs:
    for index, row in df.iterrows():
        pt[i] += row[1]
        values[i].append(row[1])
    avg_points[i] = pt[i] / games_played[i]
    i += 1

print(values)
print(avg_points)

stdev = [0,0,0,0]
conf_int = [0,0,0,0]
# 1.96 means 95%
z = 1.96
for i in range(len(avg_points)):
    stdev[i] = stats.stdev(values[i])
    conf_int[i] = z * stdev[i] / math.sqrt(len(df))

print("conf: ", conf_int)


plt.bar(left, avg_points, tick_label=labels, width=0.8, color = ['red', 'orange', 'yellow', 'green'], yerr=conf_int, capsize=7, edgecolor='black')
plt.xlabel('Players')
plt.ylabel('Avg points')
plt.title('Average points per player')
plt.savefig('avg_points.png')
plt.show()