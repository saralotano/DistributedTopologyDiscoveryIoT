import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# FIGURE 1: SIMULATION TIME
data = {'Power-law Topology': [19042, 11815, 13059, 13863],
        'Grid Topology': [12055, 11470, 11829, 12601]}

df = pd.DataFrame(data, columns=['Power-law Topology', 'Grid Topology'],
                  index=['Hop Count', 'Relayed Messages', 'Bayesian Inference', 'Random'])

ax = df.plot.bar(edgecolor='black')
for container in ax.containers:
    ax.bar_label(container)

bars = ('Hop Count', 'Relayed Messages', 'Bayesian Inference', 'Random')
x_pos = np.arange(len(bars))

# Create names on the x-axis
plt.xticks(x_pos, bars, rotation=0)

# plt.title('Topology Discovery Received and Update Messages')
plt.ylabel('Simulation Time')
plt.xlabel('Node Selection Method')

plt.show()


# FIGURE 2: TRANSMITTED BYTES
data = {'Power-law Topology': [0.41, 0.07, 0.17, 0.18],
        'Grid Topology': [0.14, 0.11, 0.18, 0.24]}

df = pd.DataFrame(data, columns=['Power-law Topology', 'Grid Topology'],
                  index=['Hop Count', 'Relayed Messages', 'Bayesian Inference', 'Random'])

ax = df.plot.bar(edgecolor='black')
for container in ax.containers:
    ax.bar_label(container)

bars = ('Hop Count', 'Relayed Messages', 'Bayesian Inference', 'Random')
x_pos = np.arange(len(bars))

# Create names on the x-axis
plt.xticks(x_pos, bars, rotation=0)

# plt.title('Topology Discovery Received and Update Messages')
plt.ylabel('Transmitted bytes [MB]')
plt.xlabel('Node Selection Method')

plt.show()
