# File to read data from csv and compute graphs with boxplo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Compute win lost plot
labels = ['Random', 'Beginner', 'Expert', 'Pro']
wins, losts = [125, 144, 59, 54], [66, 47, 132, 137]

X = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
rects1 = ax.bar(X - width/2, wins, color = 'g', width=0.25, label='Wins')
rects2 = ax.bar(X + width/2, losts, color = 'r', width=0.25, label='Losts')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Wins/Losts')
ax.set_title('Number of wins and losts per agent')
ax.set_xlabel('Agent type')
ax.set_xticks(X, labels)
ax.legend()
ax.bar_label(rects1, padding=1)
ax.bar_label(rects2, padding=1)


# Compute average points plot
#average = []

#for mode in ('random', 'beginner', 'expert', 'pro'):
    #path = 'results/' + mode +'.csv'
    #df = pd.read_csv(path)
    #average.append(df['Score'].mean())

#rect = ax.bar(X, average, width=0.25, label='Average')
#
#ax.set_ylabel('Score')
#ax.set_title('Average score per agent')
#ax.set_xlabel('Agent type')
#ax.set_xticks(X, labels)
#ax.legend()
#
#ax.bar_label(rect, padding=1)

plt.show()